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


def check_user_passwd(conn, username, password, project):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT `status`, `{}` FROM `access` WHERE `username`=%s AND `password`=%s".format(project)
        cursor.execute(query=sql, args=[username, password])
        item = cursor.fetchone()
        if item:
            return item
        else:
            return None
