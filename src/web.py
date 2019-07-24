# coding=utf-8
from flask import Flask
from flask import render_template
from config import configs
from func import merge_base_context

web = Flask(__name__)
web.config.from_object(configs['development'])


@web.route('/', methods=["GET"])
@web.route('/index', methods=["GET"])
def index():
    context = {}
    context = merge_base_context(context)
    return render_template("index.html", **context)


if __name__ == '__main__':
    web.run()
