# coding=utf-8
import os
import re
import sys
import uuid
import time
import inspect
import hashlib
import platform


# from bs4 import BeautifulSoup

def print_red(message, tag="ERROR"):
    print('\033[0;31m[{}] {}\033[0m'.format(tag, str(message)))  # 红色


def print_green(message, tag="DONE"):
    print('\033[5;32m[{}] {}\033[0m'.format(tag, str(message)))  # 绿色


def print_yellow(message, tag="WARNING"):
    print('\033[0;33m[{}] {}\033[0m'.format(tag, str(message)))  # 黄色


def print_blue(message, tag="BEG"):
    print('\033[0;34m[{}] {}\033[0m'.format(tag, str(message)))  # 深蓝色


def print_purple(message, tag="MID"):
    print('\033[0;35m[{}] {}\033[0m'.format(tag, str(message)))  # 紫色


def print_azure(message, tag="END"):
    print('\033[0;36m[{}] {}\033[0m'.format(tag, str(message)))  # 浅蓝色


def print_white(message, tag="INFO"):
    print('\033[0;37m[{}] {}\033[0m'.format(tag, str(message)))  # 白色


def unix_time(unit=1):
    return int(time.time() * unit)


def str_time(pattern='%Y-%m-%d %H:%M:%S'):
    return time.strftime(pattern, time.localtime(time.time()))


def parse_time(time_obj):
    time_format = "%d-%02d-%02d %02d:%02d"
    time_str = time_format % (time_obj.tm_year, time_obj.tm_mon,
                              time_obj.tm_mday, time_obj.tm_hour, time_obj.tm_min)
    return time_str


def timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def timestamp2unix(v_timestamp):
    return int(time.mktime(v_timestamp.timetuple()))


def unix2timestamp(u_time):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(u_time))


def func_name(fa=1):
    return inspect.stack()[fa][3]


def random_code():
    return str(uuid.uuid1()).split('-')[0]


def calc_md5(seed):
    seed = str(seed).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(seed)
    return md5.hexdigest()


def process_bar(now, total, attach=''):
    # 在窗口底部动态显示进度条
    rate = now / total
    rate_num = int(rate * 100)
    bar_length = int(rate_num / 2)
    blank = ' ' * 100
    if rate_num == 100:
        bar = 'Pid:%5d: %s%s' % (os.getpid(), attach, blank)
        bar = '\r' + bar[0:40]
        bar += '%s>%d%%\n' % ('=' * bar_length, rate_num)
    else:
        bar = 'Pid:%5d: %s%s' % (os.getpid(), attach, blank)
        bar = '\r' + bar[0:40]
        bar += '%s>%d%%' % ('=' * bar_length, rate_num)
    sys.stdout.write(bar)
    sys.stdout.flush()


# def parse_xml(data):
#     xml = re.sub(r'<!\[CDATA\[(.*)\]\]>', lambda m: m.group(1), data)
#     xml = BeautifulSoup(xml, 'lxml')
#     xml = xml.html.body.xml
#     return xml


def delete_old_file(dir_path, expire_time):
    time_now = unix_time()
    dir_path = os.path.abspath(dir_path)
    for file in os.listdir(dir_path):
        file_path = '{}/{}'.format(dir_path, file)
        creat_time = os.path.getctime(file_path)
        if time_now > creat_time + expire_time:
            os.remove(file_path)


def cpu_core():
    sys_platform = platform.system()
    if sys_platform == "Windows":
        return int(os.popen("echo %NUMBER_OF_PROCESSORS%").read())
    elif sys_platform == "Linux":
        return int(os.popen(r"cat /proc/cpuinfo | grep 'cpu cores' | uniq | awk '{print $4}'").read())
    else:
        return 0


def code_dir():
    file = os.path.abspath(__file__)
    return os.path.dirname(file)


def code_path():
    return os.path.abspath(__file__)
