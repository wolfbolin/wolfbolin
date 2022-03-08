# coding=utf-8
import pymysql.cursors

import Webpage
from .page_data import *
from flask import abort
from flask import request
from flask import current_app as app


@Webpage.webpage_blue.route('/tool/login', methods=["GET"])
@Kit.verify_passwd("web_acl")
def check_token():
    return Kit.common_rsp("Success")


@Webpage.webpage_blue.route('/tool/acl', methods=["GET"])
@Kit.verify_passwd("web_acl")
def get_tool_list():
    username = request.args.get("user", "none")

    conn = app.mysql_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM `user_acl` WHERE `username`=%s"
    cursor.execute(query=sql, args=[username])
    res = cursor.fetchone()
    access_list = []
    for k, v in res.items():
        if v == "Yes":
            access_list.append(k.split("_")[0])

    return Kit.common_rsp(access_list)


@Webpage.webpage_blue.route('/blog/selection', methods=["GET"])
def blog_data():
    # 读取缓存有效期
    conn = app.mysql_pool.connection()
    expire_time = Kit.get_app_pair(conn, "blog_data", "expire_time")
    if expire_time is None:
        expire_time = 0
    else:
        expire_time = int(expire_time)

    # 计算并更新缓存
    if expire_time <= Kit.unix_time():
        expire_time = Kit.unix_time() + 3600
        source = "fetch-{}".format(expire_time)
        feed_data = fetch_blog_feed(app.config.get('RSS')['url'])
        if feed_data is None:
            return abort(500, "Get feed list failed")
        Kit.set_app_pair(conn, "blog_data", "expire_time", str(expire_time))
        Kit.set_app_pair(conn, "blog_data", "feed_data", str(feed_data))
    else:
        source = "cache-{}".format(int(expire_time) - 3600)
        feed_data = Kit.get_app_pair(conn, "blog_data", "feed_data")
        if feed_data is None:
            return abort(500, "Read feed list failed")

    return Kit.common_rsp({
        "source": source,
        "rss_info": parse_feed_data(feed_data)
    })
