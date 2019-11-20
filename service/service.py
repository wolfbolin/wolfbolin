# coding=utf-8
import os
import Util
import time
import logging
import pymysql
import coloredlogs
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from Config import get_config
from DBUtils.PooledDB import PooledDB

from Webpage import webpage_blue

# 获取配置
app_config = get_config()
base_path = os.path.split(os.path.abspath(__file__))[0]
app_config['CACHE'] = '{}/cache'.format(base_path)

# 启动日志
log_path = '{}/log'.format(app_config['CACHE'])
log_path = '{}/{}.log'.format(log_path, Util.str_time('%Y%m%d%H%M%S'))
logging.basicConfig(filename=log_path, datefmt='%Y-%m-%d %H:%M:%S')
coloredlogs.install(fmt='%(asctime)s %(levelname)s %(message)s')

# 初始化应用
app = Flask(__name__)
app.config.from_mapping(app_config)

# 初始化连接池
# pool_config = app.config.get('POOL')
# mysql_config = app.config.get('MYSQL')
# app.mysql_pool = PooledDB(creator=pymysql, **mysql_config, **pool_config)

# 初始化路由
app.register_blueprint(webpage_blue, url_prefix='/webPage')
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


@app.errorhandler(403)
def http_forbidden(msg):
    return Util.common_rsp(str(msg)[15:], code=94030, status='forbidden')


@app.errorhandler(404)
def http_not_found(msg):
    return Util.common_rsp(str(msg)[15:], code=94040, status='not_found')


@app.errorhandler(500)
def service_error(msg):
    return Util.common_rsp(str(msg)[15:], code=95000, status='error')


if __name__ == '__main__':
    app.run(host=app_config['HOST'], port=app_config['PORT'])
    exit()
