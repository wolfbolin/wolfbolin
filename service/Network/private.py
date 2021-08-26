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

