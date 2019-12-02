# coding=utf-8
import Util
import Network
from flask import request
from flask import current_app


@Network.network_blue.route('/info/ip', methods=["GET"])
def ip_info():
    user_ip = request.headers.get('X-Real-IP', '0.0.0.0')
    return Util.common_rsp(user_ip)
