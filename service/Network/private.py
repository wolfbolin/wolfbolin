# coding=utf-8
import Kit
import pymysql
import Network
from flask import current_app as app


@Network.network_blue.route('/private/host', methods=["GET"])
@Kit.verify_passwd("private_acl")
def get_host_list():
    conn = app.mysql_pool.connection()
    sql = "SELECT * FROM `host`"
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    host_list = cursor.fetchall()

    return Kit.common_rsp(host_list)


@Network.network_blue.route('/private/port', methods=["GET"])
@Kit.verify_passwd("private_acl")
def get_port_list():
    conn = app.mysql_pool.connection()
    sql = "SELECT `port`.*, `host`.`ip` FROM `port` LEFT JOIN `host` USING(`host`)"
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rule_list = cursor.fetchall()
    rule_list.sort(key=lambda it: it['id'])

    return Kit.common_rsp(rule_list)
