# coding=utf-8
import json
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
