# coding=utf-8
import os
import re
import uuid
import time
import inspect
import hashlib


def func_name(fa=1):
    return inspect.stack()[fa][3]


def unix_time(unit=1):
    return int(time.time() * unit)


def str_time(pattern='%Y-%m-%d %H:%M:%S'):
    return time.strftime(pattern, time.localtime(time.time()))


def parse_time(time_obj):
    time_format = "%d-%02d-%02d %02d:%02d"
    time_str = time_format % (time_obj.tm_year, time_obj.tm_mon,
                              time_obj.tm_mday, time_obj.tm_hour, time_obj.tm_min)
    return time_str


def calc_md5(seed):
    seed = str(seed).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(seed)
    return md5.hexdigest()
