# coding=utf-8
import json
import Util
import Monitor
from flask import request
from Monitor import database as db
from flask import current_app as app
from .common import modify_server_domain

g_server_location_key = {"hostname", "unix_time", "server_ip"}
g_server_heartbeat_key = {"hostname", "unix_time", "boot_time"}


@Monitor.monitor_blue.route("/server/report/heartbeat", methods=["POST"])
@Util.req_check_json_key(g_server_heartbeat_key)
@Util.req_check_hostname
@Util.req_check_unixtime
@Util.verify_token
def server_report_heartbeat():
    time_now = Util.unix_time()
    server_info = request.get_json()
    conn = app.mysql_pool.connection()

    # 更新信息
    db.update_active_time(conn, server_info["hostname"], time_now)
    db.update_server_info(conn, server_info)

    result = {
        "msg": "Success;Update server info success"
    }
    if abs(time_now - int(server_info["unix_time"])) > 60:
        result["msg"] += "(The clock needs to be updated)"

    return Util.common_rsp(result)


@Monitor.monitor_blue.route("/server/report/location", methods=["POST"])
@Util.req_check_json_key(g_server_location_key)
@Util.req_check_hostname
@Util.req_check_unixtime
@Util.verify_token
def server_report_location():
    server_info = request.get_json()
    conn = app.mysql_pool.connection()

    client_ip = request.headers.get("X-Real-IP", "0.0.0.0")
    # 链路真实性验证
    if server_info["hostname"] != "test-wolfbolin" and server_info["server_ip"] != client_ip:
        return Util.common_rsp("Reject IP", status="Forbidden")

    # 检查DNS记录
    result = {
        "msg": "Nothing to do"
    }
    cache_info = db.get_monitor_info(conn, server_info["hostname"])
    if cache_info is None or cache_info["server_ip"] != server_info["server_ip"]:
        server_index = app.config.get("HOST")
        server_domain = server_index[server_info["hostname"]]
        result["msg"] = modify_server_domain(server_domain, server_info["server_ip"])
        db.update_server_ip(conn, server_info["hostname"], client_ip)

    return Util.common_rsp(result)


@Monitor.monitor_blue.route("/server/check", methods=["GET"])
def server_check():
    # 本地数据校验
    client_ip = request.headers.get("X-Real-IP", "0.0.0.0")
    if client_ip != "127.0.0.1":
        return Util.common_rsp("Reject IP", status="Forbidden")

    expire_time = 120
    time_now = Util.unix_time()
    conn = app.mysql_pool.connection()

    # 检查上报时间
    check_result = []
    server_domain = app.config.get("HOST")
    check_list = app.config.get("CHECK_LIST")
    for hostname in check_list.keys():
        if check_list[hostname] == "ignore":
            continue

        health_status = {
            "hostname": hostname
        }

        server_info = db.get_monitor_info(conn, hostname)
        if server_info is None:
            health_status["comment"] = "System not enabled"
            check_result.append(health_status)
            continue

        dt_time = abs(int(server_info["active_time"]) - time_now)
        if server_info["status"] == "online" and dt_time < expire_time:
            # 保持在线
            health_status["comment"] = "System keeps online"
            sms_msg = None
        elif server_info["status"] == "offline" and dt_time >= expire_time:
            # 保持下线
            health_status["comment"] = "System remains offline"
            sms_msg = None
        elif server_info["status"] == "online" and dt_time >= expire_time:
            # 主机下线
            db.update_host_status(conn, hostname, "offline")
            health_status["comment"] = "System offline"
            sms_msg = "异常下线"
        elif server_info["status"] == "offline" and dt_time < expire_time:
            # 主机上线
            db.update_host_status(conn, hostname, "online")
            health_status["comment"] = "System online"
            sms_msg = "恢复上线"
        else:
            app.logger.info("未知状况：status:{},dt_time:{}".format(server_info["status"], dt_time))
            health_status["comment"] = "System unknown status"
            sms_msg = None

        if sms_msg is not None:
            msg_format = "发送提醒：主机{}状态变更[{}]：active_time: {} <=> time_now: {}"
            active_time = Util.unix2timestamp(int(server_info["active_time"]))
            timestamp_now = Util.unix2timestamp(time_now)
            app.logger.info(msg_format.format(hostname, sms_msg, active_time, timestamp_now))

            # 发送短信
            sms_arg = {
                "phone_numbers": json.loads(server_info["manager"]),
                "template": app.config["SMS"]["server_alarm"],
                "params": [server_domain[hostname], Util.str_time("%H:%M:%S", time_now), sms_msg]
            }
            _, sms_msg = Util.send_sms_message(conn, **sms_arg)
            health_status["sms_res"] = sms_msg

        check_result.append(health_status)

    return Util.common_rsp(check_result)
