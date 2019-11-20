# coding=utf-8
import Util
import functools
from flask import abort
from flask import request
from flask import jsonify
from flask import current_app
from Util import database as Dao


def common_rsp(data, code=92000, status='success', rsp_format='json'):
    if rsp_format == 'text':
        return data
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
