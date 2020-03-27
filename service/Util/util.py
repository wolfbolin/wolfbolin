# coding=utf-8
import Util
import functools
from flask import abort
from flask import request
from flask import jsonify
from flask import current_app
from Util import database as Dao

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
        print('verify_user')
        t = str(request.args.get('token', 'guest'))

        conn = current_app.mysql_pool.connection()
        token = Dao.get_app_pair(conn, "auth", "token")
        if token is None:
            abort(400, "Not found token")

        md5_code = Util.calc_md5(t)
        if md5_code != token:
            abort(403, "Token error")

        return func(*args, **kwargs)

    return wrapper
