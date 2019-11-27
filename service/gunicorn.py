import multiprocessing
bind = '0.0.0.0:12864'
backlog = 64
workers = multiprocessing.cpu_count() * 2 + 1