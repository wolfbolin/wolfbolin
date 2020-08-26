# coding=utf-8
import json
import Util
import queue
import Network
import DNSPodX
from flask import abort
from flask import request
from Network import database as db
from flask import current_app as app


@Network.network_blue.route('/dns/domain', methods=["GET"])
@Util.verify_token
def get_dns_domain():
    # 读取强制刷新指令
    refresh = request.args.get("refresh", "false")

    # 读取缓存有效期
    conn = app.mysql_pool.connection()
    expire_time = Util.get_app_pair(conn, "dns_data", "domain_expire_time")
    if expire_time is None or refresh == "true":
        expire_time = 0
    else:
        expire_time = int(expire_time)

    # 计算并更新缓存
    if expire_time <= Util.unix_time():
        dns_id = app.config.get('DNSPOD')['id']
        dns_token = app.config.get('DNSPOD')['token']
        user = DNSPodX.User(dns_id, dns_token)
        domain_data, _ = user.domain_list()

        domain_list = []
        for domain in domain_data:
            if domain.name in ("tinoy.xyz", "wolfbolin.cn"):
                continue
            domain_list.append(domain.name)
        domain_list.sort(key=lambda it: len(it))

        expire_time = Util.unix_time() + 3600
        source = "fetch-{}".format(expire_time)
        Util.set_app_pair(conn, "dns_data", "expire_time", str(expire_time))
        Util.set_app_pair(conn, "dns_data", "domain_list", json.dumps(domain_list))
    else:
        source = "cache-{}".format(int(expire_time) - 3600)
        domain_list = Util.get_app_pair(conn, "dns_data", "domain_list")
        if domain_list is None:
            return abort(500, "Read feed list failed")
        domain_list = json.loads(domain_list)

    return Util.common_rsp({
        "source": source,
        "domain_list": domain_list
    })


@Network.network_blue.route('/dns/domain/<domain>/record', methods=["GET"])
@Util.verify_token
def get_domain_record(domain):
    # 读取强制刷新指令
    refresh = request.args.get("refresh", "false")

    # 读取缓存有效期
    conn = app.mysql_pool.connection()
    expire_time = Util.get_app_pair(conn, "dns_data", "{}_expire_time".format(domain))
    if expire_time is None or refresh == "true":
        expire_time = 0
    else:
        expire_time = int(expire_time)

    # 计算并更新缓存
    if expire_time <= Util.unix_time():
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
                "id": record.r_id,
            })
        record_list.sort(key=lambda r: int(r["id"]))

        expire_time = Util.unix_time() + 3600
        source = "fetch-{}".format(expire_time)
        Util.set_app_pair(conn, "dns_data", "{}_expire_time".format(domain.name), str(expire_time))
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

    return Util.common_rsp({
        "source": source,
        "record_list": res_record_list
    })


@Network.network_blue.route('/dns/domain/<domain>/record', methods=["PUT"])
@Util.verify_token
def update_domain_record(domain):
    # 解析列表数据
    record_task = request.get_data(as_text=True)
    record_task = json.loads(record_task)

    # 读取现有记录
    dns_id = app.config.get('DNSPOD')['id']
    dns_token = app.config.get('DNSPOD')['token']
    user = DNSPodX.User(dns_id, dns_token)
    domain = DNSPodX.Domain(user, domain)
    record_list, _ = domain.record_list()
    record_list.sort(key=lambda r: int(r.r_id))

    # 比对与修改数据
    it = 0
    for record in record_list:
        # 跳过NS记录
        if record.r_type in ("NS", "MX"):
            continue

        app.logger.debug("compare host record")
        app.logger.debug("{}\t{}".format(record.r_id, record.name))
        app.logger.debug("{}\t{}".format(record_task[it]["id"], record_task[it]["record"]))

        # 处理记录移位
        if record.r_id != record_task[it]["id"]:
            record.remove()
            app.logger.info("[DNS]排序删除{}.{}".format(record.name, record.domain.name))
            continue

        # 根据反馈修改
        if record_task[it]["edit"] == "none":
            it += 1
            continue

        if record_task[it]["edit"] == "deleted":
            record.remove()
            app.logger.info("[DNS]标记删除{}.{}".format(record.name, record.domain.name))
            it += 1
            continue

        if record_task[it]["edit"] == "edited":
            record.name = record_task[it]["record"]
            record.r_type = record_task[it]["type"]
            record.value = record_task[it]["value"]
            app.logger.info("[DNS]标记修改{}.{}".format(record.name, record.domain.name))
            it += 1
            continue

    for it in range(it, len(record_task)):
        if record_task[it]['edit'] == "deleted":
            app.logger.info("[DNS]排除添加{}.{}".format(record_task[it]['record'], domain.name))
            continue
        app.logger.info("[DNS]添加解析{}.{}".format(record_task[it]['record'], domain.name))
        record = DNSPodX.Record(user, domain, record_task[it]['record'], record_task[it]['type'],
                                record_task[it]['value'], "默认", 600, 0, "enabled")
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
            "id": record.r_id,
        })
    record_list.sort(key=lambda r: int(r["id"]))

    expire_time = Util.unix_time() + 3600
    source = "update-{}".format(expire_time)
    Util.set_app_pair(conn, "dns_data", "{}_expire_time".format(domain.name), str(expire_time))
    db.delete_domain_record(conn, domain.name)
    db.insert_domain_record(conn, record_list)

    # 过滤特殊类型记录
    res_record_list = []
    for record in record_list:
        if record["type"] not in ("NS", "MX"):
            res_record_list.append(record)

    return Util.common_rsp({
        "source": source,
        "record_list": res_record_list
    })
