# coding=utf-8
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

from Network import network_blue

# 启动日志
time_now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
logging.basicConfig(filename='./log/{}.log'.format(time_now), datefmt='%Y-%m-%d %H:%M:%S')
coloredlogs.install(fmt='%(asctime)s %(levelname)s %(message)s')

# 初始化服务
app = Flask(__name__)
app_config = get_config()
app.config.from_pyfile(app_config)

# 初始化连接池
pool_config = app.config.get('POOL')
mysql_config = app.config.get('MYSQL')
app.mysql_pool = PooledDB(creator=pymysql, **mysql_config, **pool_config)

# 初始化路由
app.register_blueprint(network_blue, url_prefix='/network')
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return Util.common_json('Hello, world')


@app.errorhandler(403)
def http_forbidden(msg):
    return Util.common_json(str(msg)[15:], code=94030, status='forbidden')


@app.errorhandler(404)
def http_not_found(msg):
    return Util.common_json(str(msg)[15:], code=94040, status='not_found')


@app.errorhandler(500)
def service_error(msg):
    return Util.common_json(str(msg)[15:], code=95000, status='error')


if __name__ == '__main__':
    # 启动服务
    app.run(host='127.0.0.1', port='12865')
