# coding=utf-8
import os
import Util
import pymysql
import logging
import sentry_sdk
import pymemobird
from flask import Flask
from flask_cors import CORS
from Config import get_config
from DBUtils.PooledDB import PooledDB
from qcloudsms_py import SmsMultiSender
from sentry_sdk.integrations.flask import FlaskIntegration

from Webpage import webpage_blue
from Network import network_blue
from Message import message_blue
from Monitor import monitor_blue

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
file_handler = logging.FileHandler(filename='./log/run.log', encoding="utf-8")
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
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return Util.common_rsp("Hello, world!")


@app.route('/debug/sentry')
def sentry_debug():
    Util.print_red("Test sentry: {}".format(1 / 0), tag="DEBUG")
    return Util.common_rsp("DEBUG")


@app.errorhandler(400)
def http_forbidden(msg):
    Util.print_red("{}: <HTTP 400> {}".format(Util.str_time(), msg))
    return Util.common_rsp("Bad Request", status='Bad Request')


@app.errorhandler(403)
def http_forbidden(msg):
    return Util.common_rsp(str(msg)[15:], status='Forbidden')


@app.errorhandler(404)
def http_not_found(msg):
    return Util.common_rsp(str(msg)[15:], status='Not Found')


@app.errorhandler(500)
def service_error(msg):
    Util.print_red("{}: <HTTP 500> {}".format(Util.str_time(), msg))
    return Util.common_rsp(str(msg)[15:], status='Internal Server Error')


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(host='127.0.0.1', port=12880, debug=True)
    exit()
