# coding=utf-8
import json
import Util
import Monitor
from flask import request
from flask import current_app as app
from .dns_modify import modify_server_domain

g_server_report_key = {"hostname", "boot_time", "unix_time", "server_ip"}


@Monitor.monitor_blue.route("/server/report", methods=["POST"])
def server_report():
    server_info = request.get_json()
    client_ip = request.headers.get("X-Real-IP", "0.0.0.0")

    # 消息完整性检查
    if server_info is None or set(server_info.keys()) != g_server_report_key:
        return Util.common_rsp("Reject request", status="Forbidden")

    # 主机名许可列表
    server_index = app.config.get("DOMAIN")
    if server_info["hostname"] not in server_index:
        return Util.common_rsp("Unknown server", status="Forbidden")
    else:
        server_domain = server_index[server_info["hostname"]]

    # 链路真实性验证
    if server_info["hostname"] != "test-wolfbolin" and server_info["server_ip"] != client_ip:
        return Util.common_rsp("Reject IP", status="Forbidden")

    # 时间真实性验证
    if abs(int(server_info["unix_time"]) - Util.unix_time()) > 10:
        return Util.common_rsp("Reject timestamp", status="Forbidden")

    # 连接数据库
    conn = app.mysql_pool.connection()

    # 读取主机早期信息
    result = {}
    cache_info = Util.get_monitor_info(conn, server_info["hostname"])

    # 检查DNS记录
    if cache_info is None or cache_info["server_ip"] != server_info["server_ip"]:
        result.update(modify_server_domain(server_domain, server_info["server_ip"]))
    else:
        result.update({"DNS": "Nothing to do."})

    # 检查开机时间
    sms_msg = None
    sms_arg = {"template": app.config["SMS"]["server_alarm"]}
    if cache_info is None:
        # 上线运行
        server_info["manager"] = [app.config["PHONE"]["wolfbolin"]]
        sms_arg["params"] = [server_domain, server_info["boot_time"], "上线运行"]
    else:
        cache_report_time = int(cache_info["unix_time"])
        server_report_time = int(server_info["unix_time"])
        if abs(server_report_time - cache_report_time) > 120:
            # 设备重启
            server_info["manager"] = json.loads(cache_info["manager"])
            sms_arg["params"] = [server_domain, server_info["boot_time"], "停机重启"]
        else:
            # 连续运行
            server_info["manager"] = json.loads(cache_info["manager"])
            sms_msg = "Nothing happen."
    if sms_msg is None:
        sms_arg["phone_numbers"] = server_info["manager"]
        _, sms_msg = Util.send_sms_message(conn, **sms_arg)
    result["Reboot"] = sms_msg

    # 刷新主机信息
    server_info["status"] = "online"
    server_info["manager"] = json.dumps(server_info["manager"])
    Util.set_monitor_info(conn, server_info)

    return Util.common_rsp(result)


@Monitor.monitor_blue.route("/server/check", methods=["GET"])
def server_check():
    client_ip = request.headers.get("X-Real-IP", "0.0.0.0")

    # 检查消息来源
    if client_ip != "127.0.0.1":
        return Util.common_rsp("Reject IP", status="Forbidden")

    # 连接数据库
    conn = app.mysql_pool.connection()

    # 检查上报时间
    check_result = {}
    server_domain = app.config.get("DOMAIN")
    check_list = app.config.get("CHECK_LIST")
    for hostname in check_list.keys():
        if check_list[hostname] is "ignore":
            continue
        health_status = {}
        server_info = Util.get_monitor_info(conn, hostname)
        if server_info is None:
            health_status["comment"] = "System not enabled"
            check_result[hostname] = health_status
            continue

        # 心跳时间检测
        if abs(int(server_info["unix_time"]) - Util.unix_time()) < 120:
            health_status["comment"] = "System online"
            check_result[hostname] = health_status
            continue

        # 标记主机下线
        if server_info["status"] == "online":
            sms_arg = {
                "phone_numbers": json.loads(server_info["manager"]),
                "template": app.config["SMS"]["server_alarm"],
                "params": [server_domain[hostname], Util.str_time("%H:%M:%S"), "异常下线"]
            }
            _, sms_msg = Util.send_sms_message(conn, **sms_arg)
            health_status["comment"] = "System offline"
            health_status.update(sms_msg)
            server_info["status"] = "offline"
            Util.set_monitor_info(conn, server_info)
        else:
            health_status["comment"] = "System not recovered"
        check_result[hostname] = health_status

    return Util.common_rsp(check_result)
