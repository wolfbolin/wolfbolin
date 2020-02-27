# coding=utf-8
import os
import multiprocessing

if not os.path.exists('./cache/log/'):
    os.makedirs('./cache/log/')

bind = '0.0.0.0:80'
backlog = 64
workers = multiprocessing.cpu_count()
