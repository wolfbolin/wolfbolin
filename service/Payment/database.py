# coding=utf-8
import pymysql


def read_trade_info(conn, order_id):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `payment` WHERE `id`=%s"
    cursor.execute(sql, args=[order_id])
    res = cursor.fetchone()
    if res is None:
        return {}
    else:
        return res


def read_trade_status(conn, order_id):
    cursor = conn.cursor()
    sql = "SELECT `status` FROM `payment` WHERE `id`=%s"
    cursor.execute(sql, args=[order_id])
    res = cursor.fetchone()
    if res is None:
        return "NOT_EXIST"
    else:
        return res[0]


def create_trade_order(conn, app, subject, volume, callback):
    cursor = conn.cursor()
    sql = "INSERT INTO `payment`(`app`,`subject`,`status`,`volume`,`callback`)" \
          "VALUES(%s,%s,%s,%s,%s)"
    cursor.execute(sql, args=[app, subject, "CREATE", float(volume), callback])
    conn.commit()
    return cursor.lastrowid


def update_trade_status(conn, order_id, status):
    cursor = conn.cursor()
    sql = "UPDATE `payment` SET `status`=%s WHERE `id`=%s"
    cursor.execute(sql, args=[status, order_id])
    conn.commit()
    return cursor.rowcount


def update_trade_info(conn, order_id, status, buyer, bill_id):
    cursor = conn.cursor()
    sql = "UPDATE `payment` SET `status`=%s, `buyer`=%s, `bill_id`=%s " \
          "WHERE `id`=%s AND `status` NOT IN ('SUCCEED', 'FINISHED', 'CLOSED')"
    cursor.execute(sql, args=[status, buyer, bill_id, order_id])
    conn.commit()
    return cursor.rowcount


def write_pay_log(conn, code, message, data):
    cursor = conn.cursor()
    sql = "INSERT INTO `pay_log`(`code`,`message`,`res_data`)VALUES(%s,%s,%s)"
    cursor.execute(sql, args=[code, message, str(data)])
    conn.commit()
    return cursor.lastrowid
