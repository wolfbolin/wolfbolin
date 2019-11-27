# coding=utf-8
import os
import json
import Util
import requests
from flask import current_app


def read_cache():
    folder_path = os.path.join(current_app.config.get('CACHE'), "data")
    file_path = os.path.join(folder_path, "feed.xml")
    if os.path.exists(file_path):
        cache_time = os.stat(file_path).st_mtime
        local_time = Util.unix_time()
        if local_time - cache_time < 3600:
            file = open(file_path, "r", encoding='utf-8')
            return True, file.read()  # 保持缓存
    return False, ""


def update_blog_feed(rss_url):
    folder_path = os.path.join(current_app.config.get('CACHE'), "data")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        Util.print_purple("GET => {}".format(rss_url), tag="RPC")
        http_result = requests.get(url=rss_url, timeout=10)
    except requests.exceptions.ConnectTimeout as e:
        Util.print_purple("Connect rss failed => {}".format(e), tag="RPC")
        return False, ""
    if http_result.status_code == 200:
        file_path = os.path.join(folder_path, "feed.xml")
        file = open(file_path, "w", encoding='utf-8')
        file.write(http_result.text)
        Util.print_purple("Update blog feed success", tag="RPC")
        return True, http_result.text
