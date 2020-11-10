# coding=utf-8
import Webpage
from .page_data import *
from flask import abort
from flask import current_app as app


@Webpage.webpage_blue.route('/check/token', methods=["GET"])
@Util.verify_token()
def check_token():
    return Util.common_rsp("Success")


@Webpage.webpage_blue.route('/blog/selection', methods=["GET"])
def blog_data():
    # 读取缓存有效期
    conn = app.mysql_pool.connection()
    expire_time = Util.get_app_pair(conn, "blog_data", "expire_time")
    if expire_time is None:
        expire_time = 0
    else:
        expire_time = int(expire_time)

    # 计算并更新缓存
    if expire_time <= Util.unix_time():
        expire_time = Util.unix_time() + 3600
        source = "fetch-{}".format(expire_time)
        feed_data = fetch_blog_feed(app.config.get('RSS')['url'])
        if feed_data is None:
            return abort(500, "Get feed list failed")
        Util.set_app_pair(conn, "blog_data", "expire_time", str(expire_time))
        Util.set_app_pair(conn, "blog_data", "feed_data", str(feed_data))
    else:
        source = "cache-{}".format(int(expire_time) - 3600)
        feed_data = Util.get_app_pair(conn, "blog_data", "feed_data")
        if feed_data is None:
            return abort(500, "Read feed list failed")

    return Util.common_rsp({
        "source": source,
        "rss_info": parse_feed_data(feed_data)
    })
