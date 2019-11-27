import multiprocessing

bind = '0.0.0.0:80'
backlog = 64
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = './cache/log/access.log'
errorlog = './cache/log/error.log'
