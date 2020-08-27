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
    sql = "INSERT `dns_info`(`record`,`domain`,`value`,`status`,`type`,`id`)" \
          "VALUES(%s,%s,%s,%s,%s,%s)"
    for record in record_list:
        cursor.execute(query=sql, args=[record["record"], record["domain"], record["value"],
                                        record["status"], record["type"], record["id"]])
    conn.commit()
    return cursor.rowcount


def get_domain_record(conn, domain):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT `domain`,`record`,`value`,`status`,`type`,`id` FROM `dns_info` WHERE `domain`=%s"
    cursor.execute(query=sql, args=[domain])
    return cursor.fetchall()


def read_proxy_rule(conn):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `proxy_rule`"
    cursor.execute(sql)
    return cursor.fetchall()


def update_proxy_rule(conn, rule_list):
    cursor = conn.cursor()
    sql = "REPLACE INTO `proxy_rule`(`type`,`content`,`group`) VALUES (%s,%s,%s)"
    for rule in rule_list:
        cursor.execute(query=sql, args=[rule["type"], rule["content"], rule["group"]])
    conn.commit()
    return cursor.rowcount
