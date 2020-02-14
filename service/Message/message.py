# coding=utf-8
import Util
import Message
import pymemobird
from flask import request
from flask import current_app

g_printer_message_key = {'app', 'user', 'text'}


@Message.message_blue.route("/printer/text", methods=["POST"])
def printer_text_message():
    message_info = request.get_json()

    if message_info is None or set(message_info.keys()) != g_printer_message_key:
        return Util.common_rsp("Reject request", status='Forbidden')

    app = message_info['app']
    user = message_info['user']
    text = message_info['text']
    format_time = Util.str_time()
    content = "================================\n\n"  # 32
    content += "应用：{}\n".format(app)
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
    paper = pymemobird.Paper(current_app.config['PRINTER']['access_key'])
    paper.add_text(content)
    current_app.printer.print_paper(paper)

    return Util.common_rsp("Send print message success: [{}]".format(paper.paper_id))


@Message.message_blue.route("/sms/text", methods=["POST"])
def sms_text_message():
    message_info = request.get_json()

    if message_info is None or set(message_info.keys()) != g_printer_message_key:
        return Util.common_rsp("Reject request", status='Forbidden')

    sms_arg = {
        "phone_numbers": [current_app.config['PHONE']['wolfbolin']],
        "template": current_app.config['SMS']['message_push'],
        "params": [message_info['app'], message_info['user'], message_info['text'][:12]]
    }
    sms_res, sms_msg = Util.send_sms_message(**sms_arg)

    if sms_res:
        return Util.common_rsp(sms_msg['detail'][0])
    else:
        return Util.common_rsp(sms_msg, status="Bad Gateway")
