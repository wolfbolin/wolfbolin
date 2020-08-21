# coding=utf-8
import json
import Util
import Network
import DNSPodX
from flask import abort
from flask import request
from Network import database as db
from flask import current_app as app


@Network.network_blue.route('/dns/domain', methods=["GET"])
def get_dns_domain():
    # 读取强制刷新指令
    refresh = request.args.get("refresh", None)

    # 读取缓存有效期
    conn = app.mysql_pool.connection()
    expire_time = Util.get_app_pair(conn, "dns_data", "domain_expire_time")
    if expire_time is None or refresh is not None:
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
            domain_list.append(domain.name)

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
def get_domain_record(domain):
    # 读取强制刷新指令
    refresh = request.args.get("refresh", None)

    # 读取缓存有效期
    conn = app.mysql_pool.connection()
    expire_time = Util.get_app_pair(conn, "dns_data", "{}_expire_time".format(domain))
    if expire_time is None or refresh is not None:
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

        expire_time = Util.unix_time() + 3600
        source = "fetch-{}".format(expire_time)
        Util.set_app_pair(conn, "dns_data", "{}_expire_time".format(domain.name), str(expire_time))
        db.delete_domain_record(conn, domain.name)
        db.insert_domain_record(conn, record_list)
    else:
        source = "cache-{}".format(int(expire_time) - 3600)
        record_list = db.get_domain_record(conn, domain)

    # 过滤特殊类型记录
    res_record_list = []
    for record in record_list:
        if record["type"] != "NS":
            res_record_list.append(record)

    return Util.common_rsp({
        "source": source,
        "record_list": res_record_list
    })
