# coding=utf-8
import Util
from flask import current_app
from qcloudsms_py.httpclient import HTTPError


def send_sms_message(phone_numbers, template, params):
    # 限制长度
    for i, msg in enumerate(params):
        params[i] = msg[:12]

    # 发送消息
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
