# coding=utf-8
import Kit
import functools
from flask import abort
from flask import request
from flask import jsonify
from functools import wraps
from flask import current_app
from Kit import database as db
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
            'time': Kit.unix_time(),
            'method': Kit.func_name(2),
            'timestamp': Kit.str_time(),
            'data': data
        })


def verify_token():
    def deco(func):
        @functools.wraps(func)
        def check_user_token(*args, **kwargs):
            t = str(request.args.get('token', 'guest'))

            conn = current_app.mysql_pool.connection()
            token = db.get_app_pair(conn, "auth", "token")
            if token is None:
                abort(400, "Not found token")

            md5_code = Kit.calc_md5(t)
            if md5_code != token:
                app.logger.warning("Token error：{} @ {}".format(t, request.url))
                abort(403, "Token error")

            return func(*args, **kwargs)

        return check_user_token

    return deco


def verify_passwd(p):
    def deco(func):
        @functools.wraps(func)
        def check_user_token(*args, **kwargs):
            u = str(request.args.get('user', ''))
            t = str(request.args.get('pass', ''))
            md5_t = Kit.calc_md5(t)
            conn = current_app.mysql_pool.connection()
            res = db.check_user_passwd(conn, u, md5_t, p)
            if res is None:
                app.logger.warning("Password error：{} @ {}".format(u, md5_t))
                abort(400, "Not found user")

            if res["status"] != "open":
                abort(400, "Account closed")

            if res[p] != "Yes":
                abort(400, "Account has no permission")

            return func(*args, **kwargs)

        return check_user_token

    return deco


def req_check_query_key(key_list):
    def deco(func):
        @wraps(func)
        def check_query_key(*args, **kwargs):
            server_info = dict(request.args)
            if server_info is None or set(server_info.keys()) != set(key_list):
                return Kit.common_rsp("Error request key-value", status="Forbidden")
            return func(*args, **kwargs)

        return check_query_key

    return deco


def req_check_json_key(key_list):
    def deco(func):
        @wraps(func)
        def check_json_key(*args, **kwargs):
            server_info = request.get_json()
            if server_info is None or set(server_info.keys()) != set(key_list):
                return Kit.common_rsp("Error request key-value", status="Forbidden")
            return func(*args, **kwargs)

        return check_json_key

    return deco


def req_check_hostname(func):
    @wraps(func)
    def check_hostname(*args, **kwargs):
        server_info = request.get_json()
        conn = app.mysql_pool.connection()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM `monitor` WHERE `hostname`=%s"
        cursor.execute(sql, args=[server_info["hostname"]])
        num = cursor.fetchone()[0]
        if num != 1:
            return Kit.common_rsp("Unknown server", status="Forbidden")
        return func(*args, **kwargs)

    return check_hostname


def req_check_unixtime(func):
    @wraps(func)
    def check_unixtime(*args, **kwargs):
        server_info = request.get_json()
        time_now = Kit.unix_time()
        if abs(time_now - int(server_info["unix_time"])) > 30:
            return Kit.common_rsp("The message has expired", status="Forbidden")
        return func(*args, **kwargs)

    return check_unixtime
