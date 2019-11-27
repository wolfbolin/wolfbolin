# coding=utf-8
import json
import Util
import Network
import DNSPodX
from flask import request
from flask import current_app


@Network.network_blue.route('/dns/report', methods=["POST"])
def dns_report():
    server_info = request.get_json()
    client_ip = request.headers.get('X-Real-IP', '0.0.0.0')
    if 'ip' not in server_info or server_info['ip'] != client_ip:
        return Util.common_rsp("Reject IP", status='failed')

    server_index = current_app.config.get('SERVER')
    if server_info['server'] not in server_index:
        return Util.common_rsp("Unknown server", status='failed')
    else:
        server_domain = server_index[server_info['server']]

    dns_id = current_app.config.get('DNSPOD')['id']
    dns_token = current_app.config.get('DNSPOD')['token']
    user = DNSPodX.User(dns_id, dns_token)
    domain = DNSPodX.Domain(user, "t-db.cn")
    record_list = domain.record_list()[0]
    for record in record_list:
        if record.name == server_domain:
            if record.value != client_ip:
                record.value = client_ip
                record.modify()
                return Util.common_rsp("Modify IP finish")
            else:
                Util.common_rsp("Nothing to do.")

    return Util.common_rsp("Create IP record first!")
