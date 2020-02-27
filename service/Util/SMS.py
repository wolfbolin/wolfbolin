# coding=utf-8
import Util
from flask import current_app
from qcloudsms_py.httpclient import HTTPError


def send_sms_message(conn, phone_numbers, template, params):
    # 限制长度
    for i, msg in enumerate(params):
        params[i] = msg[:12]

    # 发送消息
    message_log(conn, phone_numbers, template, params)
    try:
        sms_arg = {
            'nationcode': 86,
            'phone_numbers': phone_numbers,
            'template_id': template,
            'params': params,
            'sign': current_app.config['SMS']['sign']
        }
        sms_res = current_app.sms.send_with_param(**sms_arg)
        sms_res['message'] = "Send sms text success"
        return True, sms_res
    except HTTPError as e:
        Util.print_red(e)
    return False, {"message": "Send sms text failed."}


def message_log(conn, phone, template, params):
    cursor = conn.cursor()
    sql = "INSERT INTO `message`(`phone`,`template`,`params`,`unix_time`,`local_time`)VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query=sql, args=[str(phone), str(template), str(params), Util.unix_time(), Util.str_time()])
    conn.commit()
