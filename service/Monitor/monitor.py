# coding=utf-8
import Util
import Monitor
from flask import request
from flask import current_app as app
from .dns_modify import modify_server_domain

g_server_report_key = {"hostname", "boot_time", "unix_time", "server_ip"}


@Monitor.monitor_blue.route('/server/report', methods=["POST"])
def server_report():
    server_info = request.get_json()
    client_ip = request.headers.get('X-Real-IP', '0.0.0.0')

    # 消息完整性检查
    if server_info is None or set(server_info.keys()) != g_server_report_key:
        return Util.common_rsp("Reject request", status='Forbidden')

    # 主机名许可列表
    server_index = app.config.get('SERVER')
    if server_info["hostname"] not in server_index:
        return Util.common_rsp("Unknown server", status='Forbidden')
    else:
        server_domain = server_index[server_info["hostname"]]

    # 链路真实性验证
    if server_info["hostname"] != 'test-wolfbolin' and server_info["server_ip"] != client_ip:
        return Util.common_rsp("Reject IP", status='Forbidden')

    # 时间真实性验证
    if abs(int(server_info["unix_time"]) - Util.unix_time()) > 10:
        return Util.common_rsp("Reject timestamp", status='Forbidden')

    # 连接数据库
    conn = app.mysql_pool.connection()

    # 读取主机早期信息
    cache_info = Util.get_monitor_info(conn, server_info["hostname"])

    # 检查DNS记录
    result = {}
    if cache_info is None or cache_info["server_ip"] != server_info["server_ip"]:
        result.update(modify_server_domain(server_domain, server_info["server_ip"]))
    else:
        result.update({"DNS": "Nothing to do."})

    # 检查开机时间
    sms_arg = {
        "phone_numbers": [app.config['PHONE']['wolfbolin']],
        "template": app.config['SMS']['server_alarm']
    }
    cache_boot_time = Util.timestamp2unix(cache_info["boot_time"])
    server_boot_time = Util.timestamp2unix(server_info["boot_time"])
    if cache_info is None:
        timestamp = Util.unix2timestamp(server_info["unix_time"], "%H:%M:%S")
        sms_arg["params"] = [server_domain, timestamp, "上线运行"]
        _, sms_msg = Util.send_sms_message(**sms_arg)
    elif abs(server_boot_time - cache_boot_time) > 5:
        timestamp = Util.unix2timestamp(server_info["unix_time"], "%H:%M:%S")
        sms_arg["params"] = [server_domain, timestamp, "设备重启"]
        _, sms_msg = Util.send_sms_message(**sms_arg)
    else:
        sms_msg = "Nothing happen."
    result["Reboot"] = sms_msg

    # 刷新主机信息
    server_info["status"] = "online"
    Util.set_monitor_info(conn, server_info)

    return Util.common_rsp(result)


@Monitor.monitor_blue.route('/server/check', methods=["GET"])
def server_check():
    client_ip = request.headers.get('X-Real-IP', '0.0.0.0')

    # 检查消息来源
    if client_ip != "127.0.0.1":
        return Util.common_rsp("Reject IP", status='Forbidden')

    # 连接数据库
    conn = app.mysql_pool.connection()

    # 检查上报时间
    check_result = {}
    server_index = app.config.get('SERVER')
    check_list = app.config.get('CHECK_LIST')
    for hostname in check_list.keys():
        print(hostname)
        health_status = {}
        server_info = Util.get_monitor_info(conn, hostname)
        if server_info is None:
            health_status["comment"] = "System not enabled"
            check_result[hostname] = health_status
            continue

        # 心跳时间检测
        if abs(int(server_info["unix_time"]) - Util.unix_time()) < 180:
            health_status["comment"] = "System online"
            check_result[hostname] = health_status
            continue

        # 标记主机下线
        if server_info["status"] == "online":
            sms_arg = {
                "phone_numbers": [app.config['PHONE']['wolfbolin']],
                "template": app.config['SMS']['server_alarm'],
                "params": [server_index[hostname], Util.str_time("%H:%M:%S"), "异常下线"]
            }
            _, sms_msg = Util.send_sms_message(**sms_arg)
            health_status["comment"] = "System offline"
            health_status.update(sms_msg)
            server_info["status"] = "offline"
            Util.set_monitor_info(conn, server_info)
        else:
            health_status["comment"] = "System not recovered"
        check_result[hostname] = health_status

    return Util.common_rsp(check_result)
