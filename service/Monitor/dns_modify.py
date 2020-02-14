# coding=utf-8
import Util
import DNSPodX
from flask import current_app


def modify_server_domain(server_domain, server_ip):
    # 修改DNS信息
    dns_id = current_app.config.get('DNSPOD')['id']
    dns_token = current_app.config.get('DNSPOD')['token']
    user = DNSPodX.User(dns_id, dns_token)
    domain = DNSPodX.Domain(user, "t-db.cn")
    record_list = domain.record_list()[0]
    for record in record_list:
        if record.name == server_domain:
            record.value = server_ip
            record.modify()
            return {"DNS": "Modify IP finish."}

    return {"DNS": "Create IP record first!"}
