# coding=utf-8
from flask import Blueprint

monitor_blue = Blueprint('monitor', __name__)
from .monitor import *