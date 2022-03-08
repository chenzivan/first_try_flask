#负责用户登录的路由
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views