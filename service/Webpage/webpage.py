# coding=utf-8
import json
import Util
import Webpage
from .page_data import parse_blog_rss


@Webpage.webpage_blue.route('/blogSelection', methods=["GET"])
def blog_data():
    return Util.common_rsp(parse_blog_rss())
