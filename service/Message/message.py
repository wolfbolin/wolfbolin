# coding=utf-8
import Util
import Message
import pymemobird
from flask import request
from flask import current_app
from qcloudsms_py.httpclient import HTTPError

g_printer_message_key = {'app', 'user', 'text'}


@Message.message_blue.route("/printer/text", methods=["POST"])
def printer_text_message():
    message_info = request.get_json()

    if message_info is None or set(message_info.keys()) != g_printer_message_key:
        return Util.common_rsp("Reject request", status='Forbidden')

    app = message_info['app']
    user = message_info['user']
    text = message_info['text']
    format_time = Util.format_time()
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

    try:
        sms_arg = {
            'nationcode': 86,
            'phone_number': current_app.config['SMS']['phone'],
            'template_id': current_app.config['SMS']['template'],
            'params': [message_info['app'], message_info['user'], message_info['text'][:12]],
            'sign': current_app.config['SMS']['sign']
        }
        sms_res = current_app.sms.send_with_param(**sms_arg)
        sms_res['message'] = "Send sms text success"
        return Util.common_rsp(sms_res)
    except HTTPError as e:
        Util.print_red(e)
    return Util.common_rsp({"message": "Send sms text failed."}, status="Bad Gateway")
