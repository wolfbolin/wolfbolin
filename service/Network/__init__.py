# coding=utf-8
from flask import Blueprint

network_blue = Blueprint('network', __name__)
from .network import *
from .proxy import *
from .dnspod import *
from .private import *
from .key_value import *
