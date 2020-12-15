from flask import Blueprint

bp = Blueprint('api', __name__)

from avista_base.api import config
