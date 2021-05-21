# coding=utf-8
import json

import pymysql


def get_monitor_list(conn):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT `hostname`,`boot_time`,`active_time`,`domain`,`ip_list`,`status`,`manager`,`check` FROM `monitor`"
    cursor.execute(query=sql)
    monitor_list = cursor.fetchall()
    for item in monitor_list:
        item["ip_list"] = json.loads(item["ip_list"])
    return monitor_list


def get_monitor_info(conn, hostname):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT `hostname`,`boot_time`,`active_time`,`domain`,`ip_list`,`status`,`manager` " \
          "FROM `monitor` WHERE `hostname`=%s"
    cursor.execute(query=sql, args=[hostname])
    record = cursor.fetchone()
    record["ip_list"] = json.loads(record["ip_list"])
    return record


def update_active_time(conn, hostname, unix_time):
    cursor = conn.cursor()
    sql = "UPDATE `monitor` SET `active_time`=%s WHERE `hostname`=%s"
    cursor.execute(sql, args=[unix_time, hostname])
    conn.commit()
    return cursor.rowcount


def update_server_info(conn, server_info):
    cursor = conn.cursor()
    sql = "UPDATE `monitor` SET `boot_time`=%s WHERE `hostname`=%s"
    cursor.execute(sql, args=[server_info["boot_time"], server_info["hostname"]])
    conn.commit()
    return cursor.rowcount


def update_host_status(conn, hostname, status):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE `monitor` SET `status`=%s WHERE `hostname`=%s"
    cursor.execute(query=sql, args=[status, hostname])
    conn.commit()
    return cursor.rowcount


def update_server_ip(conn, hostname, ip_list):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE `monitor` SET `ip_list`=%s WHERE `hostname`=%s"
    cursor.execute(query=sql, args=[json.dumps(ip_list), hostname])
    conn.commit()
    return cursor.rowcount
