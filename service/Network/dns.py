# coding=utf-8
import Util
import Network
import DNSPodX
from flask import abort
from flask import session
from flask import request
from flask import current_app


@Network.network_blue.route('/dns/<domain>', methods=['GET'])
@Util.verify_user
def change_dns(domain):
    dns_config = current_app.config.get('DNSPOD', {})
    try:
        dns_user = DNSPodX.User(dns_config['id'], dns_config['token'])
        dns_domain = DNSPodX.Domain(dns_user, domain)
        record_list = dns_domain.record_list()[0]
    except DNSPodX.DNSPodApiException:
        return Util.common_json('Get DNS message error.')
    record_data = []
    for record in record_list:
        record_data.append(record.detail())
    return Util.common_json(record_data)
