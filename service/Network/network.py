# coding=utf-8
import Kit
import Network
from flask import request


@Network.network_blue.route('/info/ip', methods=["GET"])
def ip_info():
    user_ip = request.headers.get('X-Real-IP', '0.0.0.0')
    style = request.args.get("style", "json")
    if style == "json":
        return Kit.common_rsp(user_ip)
    else:
        return str(user_ip)
