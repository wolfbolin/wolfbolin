# coding=utf-8
import json
import Util
import Webpage
import feedparser
from flask import current_app


@Webpage.webpage_blue.route('/blogSelection', methods=["GET"])
def blog_data():
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
    return Util.common_rsp(rss_info)
