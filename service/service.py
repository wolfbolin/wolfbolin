# coding=utf-8
import os
import Util
import sentry_sdk
import pymemobird
from flask import Flask
from flask_cors import CORS
from Config import get_config
from qcloudsms_py import SmsSingleSender
from sentry_sdk.integrations.flask import FlaskIntegration

from Webpage import webpage_blue
from Network import network_blue
from Message import message_blue

# 获取配置
app_config = get_config()
base_path = os.path.split(os.path.abspath(__file__))[0]
app_config['CACHE'] = '{}/cache'.format(base_path)

# Sentry
sentry_sdk.init(
    dsn=app_config['SENTRY']['dsn'],
    integrations=[FlaskIntegration()]
)

# 初始化应用
app = Flask(__name__)
app.config.from_mapping(app_config)

# 初始化连接池
# pool_config = app.config.get('POOL')
# mysql_config = app.config.get('MYSQL')
# app.mysql_pool = PooledDB(creator=pymysql, **mysql_config, **pool_config)

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
app.sms = SmsSingleSender(_appid, _appkey)

# 初始化路由
app.register_blueprint(webpage_blue, url_prefix='/webpage')
app.register_blueprint(network_blue, url_prefix='/network')
app.register_blueprint(message_blue, url_prefix='/message')
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello_world():
    return Util.common_rsp("Hello, world!")


@app.route('/debug/sentry')
def sentry_debug():
    Util.print_red("Test sentry: {}".format(1 / 0), tag="DEBUG")
    return "DEBUG"


@app.errorhandler(400)
def http_forbidden(msg):
    Util.print_red("{}: <HTTP 400> {}".format(Util.format_time(), msg))
    return Util.common_rsp("Bad Request", status='Bad Request')


@app.errorhandler(403)
def http_forbidden(msg):
    return Util.common_rsp(str(msg)[15:], status='Forbidden')


@app.errorhandler(404)
def http_not_found(msg):
    return Util.common_rsp(str(msg)[15:], status='Not Found')


@app.errorhandler(500)
def service_error(msg):
    Util.print_red("{}: <HTTP 500> {}".format(Util.format_time(), msg))
    return Util.common_rsp(str(msg)[15:], status='Internal Server Error')


if __name__ == '__main__':
    app.run(host=app_config['HOST'], port=app_config['PORT'])
    exit()
