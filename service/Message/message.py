# coding=utf-8
import Kit
import Message
import pymemobird
from flask import request
from flask import current_app as app

g_printer_message_key = {"app", "user", "text"}
g_sugar_message_key = {"user", "source", "title", "text"}
g_sms_message_key = {"phone", "template", "params"}


@Message.message_blue.route("/printer/text", methods=["POST"])
@Kit.req_check_json_key(g_printer_message_key)
def printer_text_message():
    message_info = request.get_json()

    name = message_info["app"]
    user = message_info["user"]
    text = message_info["text"]
    format_time = Kit.str_time()
    content = "================================\n\n"  # 32
    content += "应用：{}\n".format(name)
    content += "来源：{}\n".format(user)
    content += "时间：{}\n".format(format_time)
    content += "--------------------------------\n\n"  # 32
    content += "{}\n".format(text)
    content += "\n================================\n"  # 32
    content += r"       _    _       _  __ " + "\n"
    content += r"      | |  | |     | |/ _|" + "\n"
    content += r"      | |  | | ___ | | |_ " + "\n"
    content += r"      | |/\| |/ _ \| |  _|" + "\n"
    content += r"      \  /\  / (_) | | |  " + "\n"
    content += r"       \/  \/ \___/|_|_|  " + "\n"

    # 生成纸条对象
    paper = pymemobird.Paper(app.config["PRINTER"]["access_key"])
    paper.add_text(content)
    app.printer.print_paper(paper)

    return Kit.common_rsp("Send print message success: [{}]".format(paper.paper_id))


@Message.message_blue.route("/sugar/text", methods=["POST"])
@Kit.req_check_json_key(g_sugar_message_key)
def sugar_message_push():
    message_info = request.get_json()

    user = message_info["user"]
    source = message_info["source"]
    title = message_info["title"]
    text = message_info["text"]

    res = Kit.send_sugar_message(app.config, user, source, title, text)

    return Kit.common_rsp(res)


@Message.message_blue.route("/sms/text", methods=["POST"])
@Kit.req_check_json_key(g_printer_message_key)
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
@Kit.req_check_json_key(g_sms_message_key)
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
