# coding=utf-8
from flask import Blueprint

payment_blue = Blueprint('payment', __name__)
from .alipay_qrcode import *
from .alipay_order import *
