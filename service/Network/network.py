# coding=utf-8
import Kit
import time
import Network
from flask import request

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


@Network.network_blue.route('/info/ip', methods=["GET"])
def ip_info():
    user_ip = request.headers.get('X-Real-IP', '0.0.0.0')
    style = request.args.get("style", "json")
    if style == "json":
        return Kit.common_rsp(user_ip)
    else:
        return str(user_ip)


@Network.network_blue.route('/generate_204', methods=HTTP_METHODS)
def network_test():
    return str("success"), 204
