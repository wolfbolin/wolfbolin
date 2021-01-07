# coding=utf-8
import pymysql


def get_monitor_info(conn, hostname):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT `hostname`,`boot_time`,`active_time`,`server_ip`,`status`,`manager` " \
          "FROM `monitor` WHERE `hostname`=%s"
    cursor.execute(query=sql, args=[hostname])
    return cursor.fetchone()


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


def update_server_ip(conn, hostname, ip):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE `monitor` SET `server_ip`=%s WHERE `hostname`=%s"
    cursor.execute(query=sql, args=[ip, hostname])
    conn.commit()
    return cursor.rowcount