# coding=utf-8
import Util
import Network
import pymemobird
from flask import request
from flask import current_app

g_printer_message_key = {'app', 'user', 'text'}


@Network.network_blue.route('/message/printer', methods=["POST"])
def printer_message():
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
    content += r" _    _       _  ________       _ _       \n"
    content += r"| |  | |     | |/ _| ___ \     | (_)      \n"
    content += r"| |  | | ___ | | |_| |_/ / ___ | |_ _ __  \n"
    content += r"| |/\| |/ _ \| |  _| ___ \/ _ \| | | '_ \ \n"
    content += r"\  /\  / (_) | | | | |_/ / (_) | | | | | |\n"
    content += r" \/  \/ \___/|_|_| \____/ \___/|_|_|_| |_|\n"

    # 生成纸条对象
    paper = pymemobird.Paper(current_app.config['PRINTER']['access_key'])
    paper.add_text(content)
    current_app.printer.print_paper(paper)

    return Util.common_rsp("Send print message success: [{}]".format(paper.paper_id))
