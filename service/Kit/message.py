# coding=utf-8
import Kit
import json
import requests
from flask import current_app as app
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
            'sign': app.config['SMS']['sign']
        }
        sms_res = app.sms.send_with_param(**sms_arg)
        sms_res['message'] = "Send sms text success"
        return True, sms_res
    except HTTPError as e:
        app.logger.error(e)
    return False, {"message": "Send sms text failed"}


def message_log(conn, phone, template, params):
    cursor = conn.cursor()
    sql = "INSERT INTO `message`(`phone`,`template`,`params`,`unix_time`,`local_time`)VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(query=sql, args=[str(phone), str(template), str(params), Kit.unix_time(), Kit.str_time()])
    conn.commit()


def send_sugar_message(config, user, title, text):
    format_time = Kit.str_time()
    content = "----\n\n"  # 32
    content += "标题：{}\n\n".format(title)
    content += "来源：{}\n\n".format(user)
    content += "时间：{}\n\n".format(format_time)
    content += "----\n\n"
    content += "{}\n\n".format(text)
    content += "----\n\n"

    token = config["SUGAR"][user]
    url = "https://sc.ftqq.com/{}.send".format(token)
    params = {
        "text": title,
        "desp": content
    }
    res = requests.get(url, params=params)
    res = json.loads(res.text)

    return res