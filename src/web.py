# coding=utf-8
import os
import json
from flask import Flask
from flask import render_template
from config import configs
from func import parse_blog_rss
from func import load_web_context
from func import merge_base_context

web = Flask(__name__)
web.config.from_object(configs['development'])
web.base_path = os.path.split(os.path.abspath(__file__))[0]


@web.route('/', methods=["GET"])
@web.route('/project', methods=["GET"])
def index():
    context = load_web_context("index")
    context['section5']['content'] = parse_blog_rss()
    context = merge_base_context(context)
    print(json.dumps(context))
    return render_template("index.html", **context)


if __name__ == '__main__':
    web.run()
