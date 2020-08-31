# coding=utf-8
import Util
import functools
from flask import abort
from flask import request
from flask import jsonify
from functools import wraps
from flask import current_app
from Util import database as db
from flask import current_app as app

rsp_code = {
    "OK": 92000,
    "Bad Request": 94000,
    "Forbidden": 94030,
    "Not Found": 94040,
    "Internal Server Error": 95000,
    "Bad Gateway": 95020
}


def common_rsp(data, status='OK'):
    if status in rsp_code.keys():
        code = rsp_code[status]
    else:
        code = 95001
    rsp_format = request.args.get('format')
    if rsp_format == 'raw':
        return data
    else:
        return jsonify({
            'code': code,
            'status': status,
            'time': Util.unix_time(),
            'method': Util.func_name(2),
            'timestamp': Util.str_time(),
            'data': data
        })


def verify_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t = str(request.args.get('token', 'guest'))
        app.logger.info("正在验证Token：{} @ {}".format(t,request.url))

        conn = current_app.mysql_pool.connection()
        token = db.get_app_pair(conn, "auth", "token")
        if token is None:
            abort(400, "Not found token")

        md5_code = Util.calc_md5(t)
        if md5_code != token:
            abort(403, "Token error")

        return func(*args, **kwargs)

    return wrapper


def req_check_json_key(key_list):
    def deco(func):
        @wraps(func)
        def check_json_key(*args, **kwargs):
            server_info = request.get_json()
            if server_info is None or set(server_info.keys()) != key_list:
                return Util.common_rsp("Error request key-value", status="Forbidden")
            return func(*args, **kwargs)

        return check_json_key

    return deco


def req_check_hostname(func):
    @wraps(func)
    def check_hostname(*args, **kwargs):
        server_info = request.get_json()
        server_index = app.config.get("HOST")
        if server_info["hostname"] not in server_index:
            return Util.common_rsp("Unknown server", status="Forbidden")
        return func(*args, **kwargs)

    return check_hostname


def req_check_unixtime(func):
    @wraps(func)
    def check_unixtime(*args, **kwargs):
        server_info = request.get_json()
        time_now = Util.unix_time()
        if abs(time_now - int(server_info["unix_time"])) > 300:
            return Util.common_rsp("The message has expired", status="Forbidden")
        return func(*args, **kwargs)

    return check_unixtime
