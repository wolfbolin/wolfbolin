# coding=utf-8
import Kit
import Message
from flask import request
from flask import current_app as app


@Message.message_blue.route("/sugar/text", methods=["POST"])
def sugar_message_push():
    msg_data = request.get_json()
    user_token = request.args.get("token", None)

    user = msg_data["user"]
    source = msg_data["source"]
    title = msg_data["title"]
    text = msg_data["text"]

    res = Kit.send_sugar_message(app.config, user, source, title, text, user_token)

    return Kit.common_rsp(res)


@Message.message_blue.route("/wechat/text", methods=["POST"])
def wechat_text_message_push():
    msg_data = request.get_json()
    conn = app.mysql_pool.connection()

    content = {"content": msg_data["title"] + "\n" + msg_data["text"]}
    res = Kit.send_wechat_message(conn, app.config, msg_data["user"], "text", content)

    return Kit.common_rsp(res)


@Message.message_blue.route("/wechat/textcard", methods=["POST"])
def wechat_textcard_message_push():
    msg_data = request.get_json()
    conn = app.mysql_pool.connection()

    description = "<div class=\"gray\">{}@{}</div>".format(msg_data["source"], Kit.str_time())
    description += "<div class=\"normal\">{}</div>".format(msg_data["text"])
    content = {
        "title": msg_data["title"],
        "description": description,
        "url": msg_data["url"],
        "btntxt": "更多"
    }
    res = Kit.send_wechat_message(conn, app.config, msg_data["user"], "textcard", content)

    return Kit.common_rsp(res)


@Message.message_blue.route("/sms/text", methods=["POST"])
def sms_message_push():
    message_info = request.get_json()

    sms_arg = {
        "phone_numbers": [app.config["PHONE"]["wolfbolin"]],
        "template": app.config["SMS"]["message_push"],
        "params": [message_info["app"], message_info["user"], message_info["text"][:12]],
        "conn": app.mysql_pool.connection()
    }
    sms_res, sms_msg = Kit.send_sms_message(**sms_arg)

    if sms_res:
        return Kit.common_rsp(sms_msg["detail"][0])
    else:
        return Kit.common_rsp(sms_msg, status="Bad Gateway")


@Message.message_blue.route("/sms/send/<phone>", methods=["POST"])
@Kit.verify_token()
def sms_message_send(phone):
    message_info = request.get_json()

    if phone is None or str(phone) != str(message_info["phone"]) or len(phone) != 11:
        return Kit.common_rsp("Reject phone number", status="Forbidden")

    if isinstance(message_info["params"], list):
        for i, item in enumerate(message_info["params"]):
            message_info["params"][i] = str(item)[:12]
    else:
        return Kit.common_rsp("Reject params", status="Forbidden")

    sms_arg = {
        "phone_numbers": [str(message_info["phone"])],
        "template": str(message_info["template"]),
        "params": message_info["params"],
        "conn": app.mysql_pool.connection()
    }
    sms_res, sms_msg = Kit.send_sms_message(**sms_arg)

    if sms_res:
        return Kit.common_rsp(sms_msg["detail"][0])
    else:
        return Kit.common_rsp(sms_msg, status="Bad Gateway")
