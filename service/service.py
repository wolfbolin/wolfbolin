# coding=utf-8
import os
import Util
import time
import pymysql
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from Config import get_config
from DBUtils.PooledDB import PooledDB

from Webpage import webpage_blue
from Network import network_blue

# 获取配置
app_config = get_config()
base_path = os.path.split(os.path.abspath(__file__))[0]
app_config['CACHE'] = '{}/cache'.format(base_path)
if not os.path.exists(app_config['CACHE']):
    os.makedirs(app_config['CACHE'])

# 初始化应用
app = Flask(__name__)
app.config.from_mapping(app_config)

# 初始化连接池
# pool_config = app.config.get('POOL')
# mysql_config = app.config.get('MYSQL')
# app.mysql_pool = PooledDB(creator=pymysql, **mysql_config, **pool_config)

# 初始化路由
app.register_blueprint(webpage_blue, url_prefix='/webpage')
app.register_blueprint(network_blue, url_prefix='/network')
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


@app.errorhandler(400)
def http_forbidden(msg):
    Util.print_red("{}: <HTTP 400> {}".format(Util.timestamp(), msg))
    return Util.common_rsp("Bad Request", status='Bad Request')


@app.errorhandler(403)
def http_forbidden(msg):
    return Util.common_rsp(str(msg)[15:], status='Forbidden')


@app.errorhandler(404)
def http_not_found(msg):
    return Util.common_rsp(str(msg)[15:], status='Not Found')


@app.errorhandler(500)
def service_error(msg):
    Util.print_red("{}: <HTTP 500> {}".format(Util.timestamp(), msg))
    return Util.common_rsp(str(msg)[15:], status='Internal Server Error')


if __name__ == '__main__':
    app.run(host=app_config['HOST'], port=app_config['PORT'])
    exit()
