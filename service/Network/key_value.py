# coding=utf-8
import json

import pymysql.cursors

import Kit
import Network
from flask import request
from flask import current_app as app


@Network.network_blue.route('/k-v/groups', methods=["GET"])
@Kit.verify_token()
def get_kv_group():
    conn = app.mysql_pool.connection()
    cursor = conn.cursor()
    sql = "SELECT DISTINCT(`app`) FROM `kvdb`"
    cursor.execute(sql)
    group_list = cursor.fetchall()
    return Kit.common_rsp([it[0] for it in group_list])


@Network.network_blue.route('/k-v/group/<group>/record', methods=["GET"])
@Kit.verify_token()
def get_kv_record(group):
    conn = app.mysql_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `kvdb` WHERE `app`=%s"
    cursor.execute(sql, args=[group])
    record_list = cursor.fetchall()
    return Kit.common_rsp([it for it in record_list])


@Network.network_blue.route('/k-v/group/<group>/record/<record>', methods=["PUT"])
@Kit.verify_token()
def put_kv_detail(group, record):
    record_info = request.get_data(as_text=True)
    record_info = json.loads(record_info)
    if record_info["key"] != record:
        return Kit.common_rsp("Record error", "Forbidden")

    conn = app.mysql_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "UPDATE `kvdb` SET `val`=%s WHERE `app`=%s AND `key`=%s"
    cursor.execute(sql, args=[record_info["val"], group, record])
    conn.commit()

    return Kit.common_rsp("Success")


@Network.network_blue.route('/k-v/group/<group>/record/<record>', methods=["POST"])
@Kit.verify_token()
def add_kv_info(group, record):
    record_info = request.get_data(as_text=True)
    record_info = json.loads(record_info)
    if record_info["key"] != record:
        return Kit.common_rsp("Record error", "Forbidden")

    conn = app.mysql_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "INSERT `kvdb`(app,key,val) VALUES (%s,%s,%s)"
    cursor.execute(sql, args=[group, record, record_info["val"]])
    conn.commit()

    return Kit.common_rsp("Success")


@Network.network_blue.route('/k-v/group/<group>/record/<record>', methods=["DELETE"])
@Kit.verify_token()
def del_kv_info(group, record):
    record_info = request.get_data(as_text=True)
    record_info = json.loads(record_info)
    if record_info["key"] != record:
        return Kit.common_rsp("Record error", "Forbidden")

    conn = app.mysql_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "DELETE FROM `kvdb` WHERE `app`=%s AND `key`=%s"
    cursor.execute(sql, args=[group, record])
    conn.commit()

    return Kit.common_rsp("Success")
