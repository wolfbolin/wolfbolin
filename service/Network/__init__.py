from flask import Blueprint
network_blue = Blueprint('Network', __name__)
from .dns import *

