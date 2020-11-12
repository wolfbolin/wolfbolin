# coding=utf-8
import json
import Kit
import Payment
import requests
from .common import *
from flask import abort
from flask import request
from Payment import database as db
from flask import current_app as app

g_trade_precreate_key = {"app", "subject", "volume"}


@Payment.payment_blue.route('/alipay', methods=["POST"])
@Kit.req_check_json_key(g_trade_precreate_key)
def trade_precreate():
    # 获取请求参数
    trade_info = request.get_json()
    if trade_info["app"] not in app.config["ALIPAY"].keys():
        return abort(400, "Error app name")
    conn = app.mysql_pool.connection()

    # 创建本地订单
    order_id = db.create_trade_order(conn, trade_info["app"], trade_info["subject"],
                                     trade_info["volume"], app.config["ALIPAY"]["notify"])
    order_str = "Bill-%08d" % order_id

    # 创建交易订单
    res, data = alipay_precreate(conn, order_str, trade_info["app"], trade_info["subject"], trade_info["volume"])
    if res.split(":")[0] == "WA":
        return abort(500, "Service {} Error".format(res.split(":")[1]))

    # 修改订单状态
    db.update_trade_status(conn, order_id, "CREATED")

    # # 生成二维码
    # qr_code = qrcode.make(data)
    # buffered = io.BytesIO()
    # qr_code.save(buffered, format="JPEG")
    # qrcode_str = base64.b64encode(buffered.getvalue()).decode()

    return Kit.common_rsp({
        "order_str": order_str,
        "expire_time": "",
        "qrcode_link": data
    })


def alipay_precreate(conn, order_str, app_name, subject, volume):
    app_id = app.config["ALIPAY"][app_name]
    # 组装请求数据
    if app_name == "test":
        alipay_key_path = "Config/dev-alipay.pub"
        url = "https://openapi.alipaydev.com/gateway.do"
    else:
        alipay_key_path = "Config/alipay.pub"
        url = "https://openapi.alipay.com/gateway.do"
    params = {
        "app_id": app_id,
        "biz_content": "",
        "charset": "utf-8",
        "method": "alipay.trade.precreate",
        "notify_url": app.config["ALIPAY"]["notify"],
        "sign_type": "RSA2",
        "timestamp": Kit.str_time(),
        "version": "1.0",
    }  # 已经完成排序
    query = {
        "out_trade_no": order_str,
        "total_amount": volume,
        "subject": subject,
        "timeout_express": "10m"
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
        Kit.print_red("requests.exceptions.ProxyError:[LOG:%s]" % log_id)
        return "WA:Local", None
    except requests.exceptions.ReadTimeout:
        log_id = db.write_pay_log(conn, "00000", "ReadTimeout", json.dumps({"url": url, "params": params}))
        Kit.print_red("requests.exceptions.ReadTimeout:[LOG:%s]" % log_id)
        return "WA:Local", None
    except requests.exceptions.ConnectionError:
        log_id = db.write_pay_log(conn, "00000", "ConnectionError", json.dumps({"url": url, "params": params}))
        Kit.print_red("requests.exceptions.ConnectionError:[LOG:%s]" % log_id)
        return "WA:Local", None

    # 读取请求响应
    response = json.loads(res.text)
    data = response["alipay_trade_precreate_response"]
    log_id = db.write_pay_log(conn, data["code"], data["msg"], res.text)
    Kit.print_purple("Alipay trade precreate: success [LOG:%s]" % log_id)

    if data["code"] != "10000":
        return "WA:Alipay", None

    # 验证签名
    sign = response["sign"]
    sign_str = json.dumps(data, separators=(',', ':'))
    sign_str = sign_str.replace("/", r"\/")
    try:
        verify_with_rsa2(sign_str, sign, alipay_key_path)
    except rsa.pkcs1.VerificationError:
        Kit.print_red("rsa.pkcs1.VerificationError:[LOG:%s]" % log_id)
        return "WA:Sign", None

    return "AC:Success", data["qr_code"]



