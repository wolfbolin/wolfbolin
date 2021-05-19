# coding=utf-8
import json
import Kit
import Network
import DNSPodX
from flask import abort
from flask import request
from Network import database as db
from flask import current_app as app


@Network.network_blue.route('/dns/domain', methods=["GET"])
@Kit.verify_token()
def get_dns_domain():
    # 读取强制刷新指令
    refresh = request.args.get("refresh", "false")

    # 读取缓存有效期
    conn = app.mysql_pool.connection()
    expire_time = Kit.get_app_pair(conn, "dns_data", "domain_expire_time")
    if expire_time is None or refresh == "true":
        expire_time = 0
    else:
        expire_time = int(expire_time)

    # 计算并更新缓存
    if expire_time <= Kit.unix_time():
        dns_id = app.config.get('DNSPOD')['id']
        dns_token = app.config.get('DNSPOD')['token']
        user = DNSPodX.User(dns_id, dns_token)
        domain_data, _ = user.domain_list()

        domain_list = []
        for domain in domain_data:
            domain_list.append(domain.name)
        domain_list.sort()

        expire_time = Kit.unix_time() + 3600
        source = "fetch-{}".format(expire_time)
        Kit.set_app_pair(conn, "dns_data", "expire_time", str(expire_time))
        Kit.set_app_pair(conn, "dns_data", "domain_list", json.dumps(domain_list))
    else:
        source = "cache-{}".format(int(expire_time) - 3600)
        domain_list = Kit.get_app_pair(conn, "dns_data", "domain_list")
        if domain_list is None:
            return abort(500, "Read feed list failed")
        domain_list = json.loads(domain_list)

    return Kit.common_rsp({
        "source": source,
        "domain_list": domain_list
    })


@Network.network_blue.route('/dns/domain/<domain>/record', methods=["GET"])
@Kit.verify_token()
def get_domain_record(domain):
    # 读取强制刷新指令
    refresh = request.args.get("refresh", "false")

    # 读取缓存有效期
    conn = app.mysql_pool.connection()
    expire_time = Kit.get_app_pair(conn, "dns_data", "{}_expire_time".format(domain))
    if expire_time is None or refresh == "true":
        expire_time = 0
    else:
        expire_time = int(expire_time)

    # 计算并更新缓存
    if expire_time <= Kit.unix_time():
        dns_id = app.config.get('DNSPOD')['id']
        dns_token = app.config.get('DNSPOD')['token']
        user = DNSPodX.User(dns_id, dns_token)
        domain = DNSPodX.Domain(user, domain)
        record_data, _ = domain.record_list()

        record_list = []
        for record in record_data:
            record_list.append({
                "domain": record.domain.name,
                "record": record.name,
                "value": record.value,
                "status": record.status,
                "type": record.r_type,
                "ttl": record.ttl,
                "id": record.r_id,
            })
        record_list.sort(key=lambda r: int(r["id"]))

        expire_time = Kit.unix_time() + 3600
        source = "fetch-{}".format(expire_time)
        Kit.set_app_pair(conn, "dns_data", "{}_expire_time".format(domain.name), str(expire_time))
        db.delete_domain_record(conn, domain.name)
        db.insert_domain_record(conn, record_list)
    else:
        source = "cache-{}".format(int(expire_time) - 3600)
        record_list = db.get_domain_record(conn, domain)
        record_list.sort(key=lambda r: int(r["id"]))

    # 过滤特殊类型记录
    res_record_list = []
    for record in record_list:
        if record["type"] not in ("NS", "MX"):
            res_record_list.append(record)

    return Kit.common_rsp({
        "source": source,
        "record_list": res_record_list
    })


@Network.network_blue.route('/dns/domain/<domain>/record', methods=["PUT"])
@Kit.verify_token()
def set_domain_record(domain):
    # 解析列表数据
    commit_record_list = request.get_data(as_text=True)
    commit_record_list = json.loads(commit_record_list)

    # 读取现有记录
    dns_id = app.config.get('DNSPOD')['id']
    dns_token = app.config.get('DNSPOD')['token']
    user = DNSPodX.User(dns_id, dns_token)
    domain = DNSPodX.Domain(user, domain)
    record_list, _ = domain.record_list()
    record_list.sort(key=lambda r: int(r.r_id))

    # 比对与修改数据
    it = 0  # 原始数据列表指针
    for record in record_list:
        # 跳过NS记录
        if record.r_type in ("NS", "MX"):
            continue

        app.logger.debug("compare host record")
        app.logger.debug("{}\t{}".format(record.r_id, record.name))
        app.logger.debug("{}\t{}".format(commit_record_list[it]["id"], commit_record_list[it]["record"]))

        # 处理记录移位
        if record.r_id != commit_record_list[it]["id"]:
            record.remove()
            app.logger.info("[DNS]排序删除{}.{}".format(record.name, record.domain.name))
            continue

        # 根据反馈删除记录
        if commit_record_list[it]["edit"] == "deleted":
            record.remove()
            app.logger.info("[DNS]标记删除{}.{}".format(record.name, record.domain.name))
            it += 1
            continue

        # 对比内容以修改
        if commit_record_list[it]["record"] != record.name \
                or commit_record_list[it]["ttl"] != record.ttl \
                or commit_record_list[it]["value"] != record.value \
                or commit_record_list[it]["type"] != record.r_type:
            record.name = commit_record_list[it]["record"]
            record.r_type = commit_record_list[it]["type"]
            record.value = commit_record_list[it]["value"]
            record.ttl = commit_record_list[it]["ttl"]
            record.modify()
            app.logger.info("[DNS]标记修改{}.{}".format(record.name, record.domain.name))
            it += 1
            continue

        it += 1  # 无变化跳过

    for it in range(it, len(commit_record_list)):
        if commit_record_list[it]['edit'] == "deleted":
            app.logger.info("[DNS]排除添加{}.{}".format(commit_record_list[it]['record'], domain.name))
            continue
        app.logger.info("[DNS]添加解析{}.{}".format(commit_record_list[it]['record'], domain.name))
        record = DNSPodX.Record(user, domain, commit_record_list[it]['record'], commit_record_list[it]['type'],
                                commit_record_list[it]['value'], "默认", 600, 0, "enabled")
        record.create()

    # 刷新DNS解析缓存
    conn = app.mysql_pool.connection()
    record_data, _ = domain.record_list()
    record_list = []
    for record in record_data:
        record_list.append({
            "domain": record.domain.name,
            "record": record.name,
            "value": record.value,
            "status": record.status,
            "type": record.r_type,
            "ttl": record.ttl,
            "id": record.r_id,
        })
    record_list.sort(key=lambda r: int(r["id"]))

    expire_time = Kit.unix_time() + 3600
    source = "update-{}".format(expire_time)
    Kit.set_app_pair(conn, "dns_data", "{}_expire_time".format(domain.name), str(expire_time))
    db.delete_domain_record(conn, domain.name)
    db.insert_domain_record(conn, record_list)

    # 过滤特殊类型记录
    res_record_list = []
    for record in record_list:
        if record["type"] not in ("NS", "MX"):
            res_record_list.append(record)

    return Kit.common_rsp({
        "source": source,
        "record_list": res_record_list
    })
