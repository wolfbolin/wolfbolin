# coding=utf-8
import DNSPodX
from flask import current_app as app


def modify_server_domain(sub_domain, ip_list):
    # 修改DNS信息
    dns_id = app.config.get('DNSPOD')['id']
    dns_token = app.config.get('DNSPOD')['token']
    user = DNSPodX.User(dns_id, dns_token)
    domain = DNSPodX.Domain(user, "ac0.ink")
    record_list = domain.record_list()[0]

    it_ip = 0
    for record in record_list:
        if record.name == sub_domain:
            record.value = ip_list[it_ip]
            record.modify()
            it_ip += 1

    if it_ip != len(ip_list):
        return "Insufficient IP records"

    return "Modify IP finish."
