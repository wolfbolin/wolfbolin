# coding=utf-8
import json
import Util
import requests
from flask import current_app


def update_blog_feed(rss_url, base_path):
    try:
        http_result = requests.get(url=rss_url, timeout=10)
    except requests.exceptions.ConnectTimeout as e:
        print("Connect rss failed => %s", e)
        return
    if http_result.status_code == 200:
        file_path = "{}/data/feed.xml".format(base_path)
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(http_result.text)
            print("Update blog feed success")
