# coding=utf-8
from flask import Blueprint

network_blue = Blueprint('network', __name__)
from .network import *
from .clash import *
from .dnspod import *
