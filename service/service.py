# coding=utf-8
import os
import Kit
import pymysql
import logging
import sentry_sdk
import pymemobird
from flask import Flask
from flask import request
from flask_cors import CORS
from Config import get_config
from dbutils.pooled_db import PooledDB
from qcloudsms_py import SmsMultiSender
from logging.handlers import TimedRotatingFileHandler
from sentry_sdk.integrations.flask import FlaskIntegration

from Webpage import webpage_blue
from Network import network_blue
from Message import message_blue
from Monitor import monitor_blue
from Payment import payment_blue

# 获取配置
app_config = get_config()
base_path = os.path.split(os.path.abspath(__file__))[0]

# Sentry
sentry_sdk.init(
    dsn=app_config['SENTRY']['dsn'],
    integrations=[FlaskIntegration()],
    environment=app_config["RUN_ENV"]
)

# 初始化应用
app = Flask(__name__)
app.config.from_mapping(app_config)

# 服务日志
file_logger = logging.getLogger('file_log')
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename='{}/log/run.log'.format(base_path), encoding="utf-8")
file_handler.setFormatter(logging.Formatter('%(asctime)s:<%(levelname)s> %(message)s'))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# 初始化连接池
for key in app.config.get('POOL').keys():
    app.config.get('POOL')[key] = int(app.config.get('POOL')[key])
app.config.get('MYSQL')["port"] = int(app.config.get('MYSQL')["port"])
pool_config = app.config.get('POOL')
mysql_config = app.config.get('MYSQL')
app.mysql_pool = PooledDB(creator=pymysql, **mysql_config, **pool_config)

# 初始化打印机
pymemobird.http_proxy = app.config['PROXY']['http_proxy']
_key = app.config['PRINTER']['access_key']
_id = app.config['PRINTER']['user_identify']
_user = pymemobird.User(_key, _id)
_machine = app.config['PRINTER']['memobird_id']
_device = pymemobird.Device(_machine)
_device.bind_user(_user)
app.printer = _device

# 初始化SMS
_appid = app.config['SMS']['appid']
_appkey = app.config['SMS']['appkey']
app.sms = SmsMultiSender(_appid, _appkey)

# 初始化路由
app.register_blueprint(webpage_blue, url_prefix='/webpage')
app.register_blueprint(network_blue, url_prefix='/network')
app.register_blueprint(message_blue, url_prefix='/message')
app.register_blueprint(monitor_blue, url_prefix='/monitor')
app.register_blueprint(payment_blue, url_prefix='/payment')
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return Kit.common_rsp("Hello, world!")


@app.route('/debug/sentry')
def sentry_debug():
    app.logger.info("[DEBUG]Test sentry: {}".format(1 / 0))
    return Kit.common_rsp("DEBUG")


@app.errorhandler(400)
def http_forbidden(msg):
    app.logger.warning("{}: <HTTP 400> {}".format(request.url, msg))
    return Kit.common_rsp("Bad Request", status='Bad Request')


@app.errorhandler(403)
def http_forbidden(msg):
    return Kit.common_rsp(str(msg)[15:], status='Forbidden')


@app.errorhandler(404)
def http_not_found(msg):
    return Kit.common_rsp(str(msg)[15:], status='Not Found')


@app.errorhandler(500)
def service_error(msg):
    app.logger.error("{}: <HTTP 500> {}".format(request.url, msg))
    return Kit.common_rsp(str(msg)[15:], status='Internal Server Error')


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port=12880, debug=True)
    exit()
