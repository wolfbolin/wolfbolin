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


def send_sugar_message(config, user, source, title, text, token=None):
    format_time = Kit.str_time()
    content = "----\n\n"  # 32
    content += "标题：{}\n\n".format(title)
    content += "来源：{}\n\n".format(source)
    content += "时间：{}\n\n".format(format_time)
    content += "----\n\n"
    content += "{}\n\n".format(text)
    content += "----\n\n"

    if token is None:
        token = config["SUGAR"][user]
    url = "https://sctapi.ftqq.com/{}.send".format(token)
    params = {
        "text": title,
        "desp": content
    }
    res = requests.get(url, params=params)
    res = json.loads(res.text)

    return res


def send_wechat_message(conn, config, user, m_type, content):
    access_token = get_wechat_token(conn, config)
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
    param = {"access_token": access_token}
    data = {
        "touser": user,
        "msgtype": m_type,
        "agentid": config["WECHAT"]["agentid"],
        m_type: content,
        "safe": 1
    }
    res = requests.post(url, params=param, json=data)
    return json.loads(res.text)


def get_wechat_token(conn, config):
    token_expire = Kit.get_app_pair(conn, "message", "wechat_token_expire")
    if token_expire is None or Kit.unix_time() > int(token_expire):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        param = {
            "corpid": config["WECHAT"]["corpid"],
            "corpsecret": config["WECHAT"]["corpsecret"],
        }
        res = requests.get(url, params=param)
        res = json.loads(res.text)
        access_token = res["access_token"]
        Kit.set_app_pair(conn, "message", "wechat_access_token", access_token)
        Kit.set_app_pair(conn, "message", "wechat_token_expire", Kit.unix_time() + 3600)
    else:
        access_token = Kit.get_app_pair(conn, "message", "wechat_access_token")
    return access_token
