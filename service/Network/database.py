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
    sql = "INSERT `dns_info`(`record`,`domain`,`value`,`status`,`type`,`ttl`,`id`)" \
          "VALUES(%s,%s,%s,%s,%s,%s,%s)"
    for record in record_list:
        cursor.execute(query=sql, args=[record["record"], record["domain"], record["value"],
                                        record["status"], record["type"], record["ttl"], record["id"]])
    conn.commit()
    return cursor.rowcount


def get_domain_record(conn, domain):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT `domain`,`record`,`value`,`status`,`type`,`ttl`,`id` FROM `dns_info` WHERE `domain`=%s"
    cursor.execute(query=sql, args=[domain])
    return list(cursor.fetchall())


def read_proxy_rule(conn, user):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `proxy_rule` WHERE `user`=%s"
    cursor.execute(sql, args=[user])
    return cursor.fetchall()


def update_proxy_rule(conn, username, rule_list):
    cursor = conn.cursor()
    sql = "DELETE FROM `proxy_rule` WHERE `user`=%s"
    cursor.execute(query=sql, args=[username])
    sql = "REPLACE INTO `proxy_rule`(`user`,`type`,`content`,`group`) VALUES (%s,%s,%s,%s)"
    for rule in rule_list:
        cursor.execute(query=sql, args=[username, rule["type"], rule["content"], rule["group"]])
    conn.commit()
    return cursor.rowcount
