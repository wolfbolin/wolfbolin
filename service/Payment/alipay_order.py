# coding=utf-8
import json
import Util
import Payment
import requests
from .common import *
from flask import abort
from flask import request
from Payment import database as db
from flask import current_app as app

g_trade_query_key = {"app", "order_str"}
g_trade_status_index = {
    "WAIT_BUYER_PAY": "WAITING",
    "TRADE_SUCCESS": "SUCCESS",
    "TRADE_FINISHED": "FINISHED",
    "TRADE_CLOSED": "CLOSED",
}


@Payment.payment_blue.route('/alipay/notify', methods=["POST"])
@Util.verify_token("alipay")
def trade_notify():
    notify_data = dict(request.args)
    # 验证请求参数
    if "sign" not in notify_data.keys():
        return "Who are you?"
    conn = app.mysql_pool.connection()
    log_id = db.write_pay_log(conn, "00000", "alipay.notify", json.dumps(notify_data, ensure_ascii=False))
    Util.print_purple("Trade notify receive:[LOG:%s]" % log_id)

    # 整理验签数据
    sign = notify_data["notify_data"]
    notify_data.pop("sign_type")
    notify_data = dict(sorted(notify_data.items()))
    sign_str = "&".join(["{}={}".format(key, val) for key, val in notify_data.items()])
    try:
        verify_with_rsa2(sign_str, sign)
    except rsa.pkcs1.VerificationError:
        Util.print_red("rsa.pkcs1.VerificationError:[LOG:%s]" % log_id)
        return "WA:Sign", None

    return "OK"


@Payment.payment_blue.route('/alipay', methods=["GET"])
@Util.req_check_json_key(g_trade_query_key)
@Util.verify_token("security")
def trade_query():
    # 获取请求参数
    trade_info = request.get_json()
    if trade_info["app"] not in app.config["ALIPAY"].keys():
        return abort(400, "Error app name")
    conn = app.mysql_pool.connection()

    # 查询订单状态
    order_str = trade_info["order_str"]
    res, data = alipay_query(conn, order_str, trade_info["app"])
    if res.split(":")[0] == "WA":
        return abort(500, "Service {} Error".format(res.split(":")[1]))

    # 修改订单状态
    order_id = order_str.replace("Bill-", "")
    db.update_trade_status(conn, order_id, g_trade_status_index[data[2]])
    db.update_trade_info(conn, order_id, data[0], data[1])

    return Util.common_rsp({
        "order_str": order_str,
        "order_status": g_trade_status_index[data[2]]
    })


def alipay_query(conn, order_str, app_name):
    app_id = app.config["ALIPAY"][app_name]
    # 组装请求数据
    if app_name == "test":
        alipay_key_path = "config/dev-alipay.pub"
        url = "https://openapi.alipaydev.com/gateway.do"
    else:
        alipay_key_path = "config/alipay.pub"
        url = "https://openapi.alipay.com/gateway.do"
    params = {
        "app_id": app_id,
        "biz_content": "",
        "charset": "utf-8",
        "method": "alipay.trade.query",
        "sign_type": "RSA2",
        "timestamp": Util.str_time(),
        "version": "1.0"
    }  # 已经完成排序
    query = {
        "out_trade_no": order_str,
    }
    params["biz_content"] = json.dumps(query)

    # 生成请求签名
    params = dict(sorted(params.items()))
    sign_str = "&".join(["{}={}".format(key, val) for key, val in params.items()])
    params["sign"] = sign_with_rsa2(sign_str)

    # 发送创建请求
    try:
        res = requests.get(url=url, params=params)
    except requests.exceptions.ProxyError:
        log_id = db.write_pay_log(conn, "00000", "ProxyError", json.dumps({"url": url, "params": params}))
        Util.print_red("requests.exceptions.ProxyError:[LOG:%s]" % log_id)
        return "WA:Local", None
    except requests.exceptions.ReadTimeout:
        log_id = db.write_pay_log(conn, "00000", "ReadTimeout", json.dumps({"url": url, "params": params}))
        Util.print_red("requests.exceptions.ReadTimeout:[LOG:%s]" % log_id)
        return "WA:Local", None
    except requests.exceptions.ConnectionError:
        log_id = db.write_pay_log(conn, "00000", "ConnectionError", json.dumps({"url": url, "params": params}))
        Util.print_red("requests.exceptions.ConnectionError:[LOG:%s]" % log_id)
        return "WA:Local", None

    # 读取请求响应
    response = json.loads(res.text)
    data = response["alipay_trade_query_response"]
    log_id = db.write_pay_log(conn, data["code"], data["msg"], res.text)
    Util.print_purple("Trade precreate success:[LOG:%s]" % log_id)

    if data["code"] != "10000":
        return "WA:Alipay", None

    # 验证签名
    sign = response["sign"]
    sign_str = json.dumps(data, separators=(',', ':'))
    sign_str = sign_str.replace("/", r"\/")
    try:
        verify_with_rsa2(sign_str, sign, alipay_key_path)
    except rsa.pkcs1.VerificationError:
        Util.print_red("rsa.pkcs1.VerificationError:[LOG:%s]" % log_id)
        return "WA:Sign", None

    return "AC:Success", (data["buyer_logon_id"], data["trade_no"], data["trade_status"])
