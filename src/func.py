# coding=utf-8
import json
import datetime
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


def parse_blog_rss():
    rss_url = current_app.config.get('RSS')
    rss = feedparser.parse(rss_url)
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
