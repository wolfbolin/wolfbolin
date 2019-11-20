# coding=utf-8
import json
import Util
import requests
import feedparser
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


def parse_blog_rss():
    base_path = current_app.config.get('CACHE')
    file_path = "{}/webpage/feed.xml".format(base_path)
    rss = feedparser.parse(file_path)
    rss_info = []
    tag_url = "https://blog.wolfbolin.com/archives/tag/%s"
    for item in rss.entries[:9]:
        time = Util.parse_time(item.published_parsed)
        tag_list = [(tag_url % tag.term, tag.term) for tag in item.tags]
        desc_text = item.description.replace("&#46;&#46;&#46;", "...")
        rss_info.append({
            "time": time,
            "tags": tag_list,
            "link": item.link,
            "desc": desc_text,
            "title": item.title
        })
    return rss_info
