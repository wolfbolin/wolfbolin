# coding=utf-8
import pymysql


def set_app_pair(conn, app, key, val):
    with conn.cursor() as cursor:
        sql = "REPLACE INTO `kvdb` (`app`,`key`,`val`) VALUES (%s,%s,%s)"
        cursor.execute(query=sql, args=[app, key, val])
        conn.commit()
        return cursor.rowcount


def get_app_pair(conn, app, key):
    with conn.cursor() as cursor:
        sql = "SELECT `key`, `val` FROM `kvdb` WHERE `app`=%s AND `key`=%s"
        cursor.execute(query=sql, args=[app, key])
        item = cursor.fetchone()
        if item and key == item[0]:
            return item[1]
        else:
            return None


def set_monitor_info(conn, data):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "REPLACE INTO `monitor`(`hostname`,`boot_time`,`unix_time`,`server_ip`,`status`,`manager`)" \
          "VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query=sql, args=[data["hostname"], data["boot_time"], data["unix_time"],
                                    data["server_ip"], data["status"], data["manager"]])
    conn.commit()
    return cursor.rowcount


def set_host_offline(conn, hostname):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE `monitor` SET `status`='offline' WHERE `hostname`=%s"
    cursor.execute(query=sql, args=[str(hostname)])
    conn.commit()
    return cursor.rowcount


def get_monitor_info(conn, hostname):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT `hostname`,`boot_time`,`unix_time`,`server_ip`,`status`,`manager` FROM `monitor` WHERE `hostname`=%s"
    cursor.execute(query=sql, args=[hostname])
    return cursor.fetchone()
