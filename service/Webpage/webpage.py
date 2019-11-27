# coding=utf-8
import json
import Util
import Webpage
import feedparser
from .page_data import *
from flask import abort
from flask import current_app


@Webpage.webpage_blue.route('/blogSelection', methods=["GET"])
def blog_data():
    cache_status, feed_data = read_cache()
    if not cache_status:
        update_status, feed_data = update_blog_feed(current_app.config.get('RSS')['url'])
        if not update_status:
            return abort(500, "Get feed list failed")

    rss = feedparser.parse(feed_data)
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
