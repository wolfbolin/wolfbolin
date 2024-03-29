# coding=utf-8
import json
import Kit
import Monitor
from flask import request
from Monitor import database as db
from flask import current_app as app
from .common import modify_server_domain


@Monitor.monitor_blue.route("/server/report/heartbeat", methods=["POST"])
@Kit.req_check_json_key({"hostname", "unix_time", "boot_time"})
@Kit.req_check_hostname
@Kit.req_check_unixtime
@Kit.verify_token()
def server_report_heartbeat():
    time_now = Kit.unix_time()
    server_info = request.get_json()
    conn = app.mysql_pool.connection()

    # 更新信息
    db.update_active_time(conn, server_info["hostname"], time_now)
    db.update_server_info(conn, server_info)

    result = {
        "msg": "Success;Update server info success"
    }
    if abs(time_now - int(server_info["unix_time"])) > 30:
        result["msg"] += "(The clock needs to be updated)"

    return Kit.common_rsp(result)


@Monitor.monitor_blue.route("/server/report/location", methods=["POST"])
@Kit.req_check_json_key({"hostname", "unix_time", "ip_list"})
@Kit.req_check_hostname
@Kit.req_check_unixtime
@Kit.verify_token()
def server_report_location():
    server_info = request.get_json()
    conn = app.mysql_pool.connection()

    # 检查DNS记录
    result = {
        "msg": "Nothing to do"
    }
    cache_info = db.get_monitor_info(conn, server_info["hostname"])
    if cache_info is None:
        result["msg"] = "Create config record first"
    elif cache_info["ip_list"] != server_info["ip_list"]:
        server_domain = cache_info["domain"]
        result["msg"] = modify_server_domain(server_domain, server_info["ip_list"])
        db.update_server_ip(conn, server_info["hostname"], server_info["ip_list"])

    return Kit.common_rsp(result)


@Monitor.monitor_blue.route("/server/check", methods=["GET"])
@Kit.verify_token()
def server_check():
    # 本地数据校验
    client_ip = request.headers.get("X-Real-IP", "0.0.0.0")
    if client_ip != "127.0.0.1":
        return Kit.common_rsp("Reject IP", status="Forbidden")

    expire_time = 120
    time_now = Kit.unix_time()
    conn = app.mysql_pool.connection()

    # 检查上报时间
    check_result = []
    monitor_list = db.get_monitor_list(conn)
    for monitor_record in monitor_list:
        if monitor_record["check"] == "ignore":
            continue

        health_status = {
            "hostname": monitor_record["hostname"]
        }

        if monitor_record is None:
            health_status["comment"] = "System not enabled"
            check_result.append(health_status)
            continue

        dt_time = abs(int(monitor_record["active_time"]) - time_now)
        if monitor_record["status"] == "online" and dt_time < expire_time:
            # 保持在线
            health_status["comment"] = "System keeps online"
            msg_text = None
        elif monitor_record["status"] == "offline" and dt_time >= expire_time:
            # 保持下线
            health_status["comment"] = "System remains offline"
            msg_text = None
        elif monitor_record["status"] == "online" and dt_time >= expire_time:
            # 主机下线
            db.update_host_status(conn, monitor_record["hostname"], "offline")
            health_status["comment"] = "System offline"
            msg_text = "异常下线"
        elif monitor_record["status"] == "offline" and dt_time < expire_time:
            # 主机上线
            db.update_host_status(conn, monitor_record["hostname"], "online")
            health_status["comment"] = "System online"
            msg_text = "恢复上线"
        else:
            app.logger.info("未知状况：status:{},dt_time:{}".format(monitor_record["status"], dt_time))
            health_status["comment"] = "System unknown status"
            msg_text = None

        if msg_text is not None:
            msg_format = "发送提醒：主机{}状态变更[{}]：active_time: {} <=> time_now: {}"
            active_time = Kit.unix2timestamp(int(monitor_record["active_time"]))
            timestamp_now = Kit.unix2timestamp(time_now)
            app.logger.info(msg_format.format(monitor_record["hostname"], msg_text, active_time, timestamp_now))

            # 发送提示
            user_list = json.loads(monitor_record["manager"])
            text = "设备状态变化\n\n" + \
                   "服务主机：{}\n\n" + \
                   "服务域名：{}\n\n" + \
                   "状态变化：{}\n\n" + \
                   "网络信息：{}\n\n" + \
                   "活跃时间：{}\n\n" + \
                   "启动时间：{}\n\n"
            text = text.format(monitor_record["hostname"], monitor_record["domain"], msg_text,
                               "/".join(monitor_record["ip_list"]),
                               Kit.unix2timestamp(monitor_record["active_time"]), monitor_record["boot_time"])
            health_status["msg_res"] = []
            for user in user_list:
                msg_res = Kit.send_wechat_message(conn, app.config, user, "service", text)
                health_status["msg_res"].append(msg_res)

        check_result.append(health_status)

    return Kit.common_rsp(check_result)
