# coding=utf-8


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
    with conn.cursor() as cursor:
        sql = "REPLACE INTO `monitor`(`hostname`,`boot_time`,`unix_time`,`server_ip`)" \
              "VALUES (%s, %s, %s, %s)"
        cursor.execute(query=sql, args=[data["hostname"], data["boot_time"], data["unix_time"], data["server_ip"]])
        conn.commit()
        return cursor.rowcount


def get_monitor_info(conn, hostname):
    with conn.cursor() as cursor:
        sql = "SELECT `hostname`,`boot_time`,`unix_time`,`server_ip` FROM `monitor` WHERE `hostname`=%s"
        cursor.execute(query=sql, args=[hostname])
        item = cursor.fetchone()
        if item and hostname == item[0]:
            return {
                "hostname": item[0],
                "boot_time": item[1],
                "unix_time": item[2],
                "server_ip": item[3]
            }
        else:
            return None
