# coding=utf-8
import pymysql


def delete_domain_record(conn, domain):
    cursor = conn.cursor()
    sql = "DELETE FROM `dns_info` WHERE `domain`=%s"
    cursor.execute(query=sql, args=[domain])
    conn.commit()
    return cursor.rowcount


def insert_domain_record(conn, record_list):
    cursor = conn.cursor()
    sql = "INSERT `dns_info`(`domain`,`record`,`value`,`status`,`type`,`id`)" \
          "VALUES(%s,%s,%s,%s,%s,%s)"
    for record in record_list:
        cursor.execute(query=sql, args=[record["domain"], record["record"], record["value"],
                                        record["status"], record["type"], record["id"]])
    conn.commit()
    return cursor.rowcount


def get_domain_record(conn, domain):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT `domain`,`record`,`value`,`status`,`type`,`id` FROM `dns_info` WHERE `domain`=%s"
    cursor.execute(query=sql, args=[domain])
    return cursor.fetchall()
