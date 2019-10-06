# coding=utf-8
from flask import Blueprint

webpage_blue = Blueprint('webpage', __name__)
from .webpage import *
