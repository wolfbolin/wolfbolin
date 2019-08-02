# coding=utf-8
import json
import requests
import feedparser
from flask import current_app
from flask import request


def merge_base_context(context):
    context['copyright'] = current_app.config.get('COPYRIGHT')
    context['nav_item'] = current_app.config.get('NAV_ITEM')
    for item in context['nav_item']:
        if item['href'] == request.path:
            item['class'] = 'wb-active'
        else:
            item['class'] = ''
    return context


def load_web_context(name):
    file_path = "{}/data/{}.json".format(current_app.base_path, name)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.loads(file.read())


def parse_time(time_obj):
    time_format = "%d-%02d-%02d %02d:%02d"
    time = time_format % (time_obj.tm_year, time_obj.tm_mon,
                          time_obj.tm_mday, time_obj.tm_hour, time_obj.tm_min)
    return time


def update_blog_feed(rss_url):
    try:
        http_result = requests.get(url=rss_url, timeout=10)
    except requests.exceptions.ConnectTimeout as e:
        print("Connect rss failed => %s", e)
        return
    if http_result.status_code == 200:
        file_path = "{}/data/feed.xml".format(current_app.base_path)
        with open(file_path, "w") as file:
            file.write(http_result.text)


def parse_blog_rss():
    file_path = "{}/data/feed.xml".format(current_app.base_path)
    rss = feedparser.parse(file_path)
    rss_info = []
    tag_url = "https://blog.wolfbolin.com/archives/tag/%s"
    for item in rss.entries[:9]:
        time = parse_time(item.published_parsed)
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
