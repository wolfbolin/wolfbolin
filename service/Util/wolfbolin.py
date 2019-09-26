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


def timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def calc_md5(seed):
    seed = str(seed).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(seed)
    return md5.hexdigest()
