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
