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


def verify_user(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('verify_user')
        user = str(request.args.get('user', 'guest'))
        code = str(request.args.get('code', ''))
        if code == '':
            abort(403, 'Empty password')

        conn = current_app.mysql_pool.connection()
        key = Dao.get_user_key(conn, user)
        if key == '':
            abort(403, 'User unregistered or incorrect password')

        md5_code = Util.calc_md5('{}{}'.format(user, key))
        if md5_code != code:
            abort(403, 'User unregistered or incorrect password')

        return func(*args, **kwargs)

    return wrapper


def timing_verify(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('verify_user')
        user = str(request.args.get('user', 'guest'))
        code = str(request.args.get('code', ''))
        timestamp = int(request.args.get('timestamp', '0'))
        if code == '':
            abort(403, 'Empty password')
        if abs(timestamp - Util.unix_time()) > 60:
            abort(403, 'Access time timeout')

        conn = current_app.mysql_pool.connection()
        key = Dao.get_user_key(conn, user)
        if key == '':
            abort(403, 'User unregistered or incorrect password')

        md5_code = Util.calc_md5('{}{}{}'.format(user, timestamp, key))
        if md5_code != code:
            abort(403, 'User unregistered or incorrect password')

        return func(*args, **kwargs)

    return wrapper
