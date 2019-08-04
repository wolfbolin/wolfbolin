# coding=utf-8
import os
import json
from flask import Flask
from flask import render_template
from config import configs
from func import parse_blog_rss
from func import load_web_context
from func import update_blog_feed
from func import merge_base_context
from flask_apscheduler import APScheduler

web = Flask(__name__)


@web.route('/', methods=["GET"])
@web.route('/project', methods=["GET"])
def index():
    context = load_web_context("index")
    context['section5']['content'] = parse_blog_rss()
    context = merge_base_context(context)
    return render_template("index.html", **context)


if __name__ == '__main__':
    if 'WEB_ENVIRONMENT' in os.environ and os.environ['WEB_ENVIRONMENT'] in configs:
        web.config.from_object(configs[os.environ['WEB_ENVIRONMENT']])
    else:
        web.config.from_object(configs['production'])
    scheduler = APScheduler()
    scheduler.init_app(web)
    scheduler.start()
    web.run()
