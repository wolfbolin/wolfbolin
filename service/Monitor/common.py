# coding=utf-8
import DNSPodX
from flask import current_app as app


def modify_server_domain(server_domain, server_ip):
    # 修改DNS信息
    dns_id = app.config.get('DNSPOD')['id']
    dns_token = app.config.get('DNSPOD')['token']
    user = DNSPodX.User(dns_id, dns_token)
    domain = DNSPodX.Domain(user, "t-db.cn")
    record_list = domain.record_list()[0]
    for record in record_list:
        if record.name == server_domain:
            record.value = server_ip
            record.modify()
            return "Modify IP finish."

    return "Create IP record first!"
