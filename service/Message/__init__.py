# coding=utf-8
from flask import Blueprint

message_blue = Blueprint('message', __name__)
from .message import *
