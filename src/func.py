# coding=utf-8
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
