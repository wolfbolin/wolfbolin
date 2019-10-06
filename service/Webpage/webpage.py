# coding=utf-8
import json
import Util
import Webpage
from flask import render_template
from .data_loader import parse_blog_rss
from .data_loader import load_webpage_data


# @Webpage.webpage_blue.route('/', methods=["GET"])
# def index():
#     base_context = load_webpage_data("base")
#     index_context = load_webpage_data("index")
#     base_context['nav_item'][0]['class'] = 'wb-active'
#     index_context['section5']['content'] = parse_blog_rss()
#     context = dict(**base_context, **index_context)
#     return render_template("index.html", **context)


@Webpage.webpage_blue.route('/webData/blogSelection', methods=["GET"])
def blog_data():
    return Util.common_rsp(parse_blog_rss())
