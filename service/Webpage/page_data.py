# coding=utf-8
import os
import json
import Util
import requests
import feedparser
from bs4 import BeautifulSoup
from flask import current_app


def fetch_blog_feed(rss_url):
    try:
        Util.print_purple("GET => {}".format(rss_url), tag="RPC")
        http_result = requests.get(url=rss_url, timeout=10)
    except requests.exceptions.ConnectTimeout as e:
        Util.print_purple("Connect rss failed => {}".format(e), tag="RPC")
        return None
    if http_result.status_code == 200:
        return http_result.text


def parse_feed_data(feed_data):
    rss = feedparser.parse(feed_data)
    rss_info = []
    tag_url = "https://blog.wolfbolin.com/archives/tag/%s"
    for item in rss.entries[:16]:
        time = Util.format_time(item.published_parsed)
        tag_list = [(tag_url % tag.term, tag.term) for tag in item.tags]
        content = BeautifulSoup(item.content[0]["value"], 'lxml')
        desc_text = "".join([it for it in content.stripped_strings])
        if len(desc_text) > 128:
            desc_text = desc_text[:128] + "..."
        rss_info.append({
            "time": time,
            "tags": tag_list,
            "link": item.link,
            "desc": desc_text,
            "title": item.title
        })
    return rss_info
