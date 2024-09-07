# -*- coding: utf-8 -*-
"""
    @file: __init__.py
    @Author:Wang Shihan
    @Date:2022/5/26
    @Description: package
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_moment import Moment
from flask_scss import Scss
from flask_mail import Mail
from flask_caching import Cache
from flask_wtf import CSRFProtect
from flask_minify import Minify
from werkzeug.routing import BaseConverter
from Mylog.log import Logger
from Mylog.jwt import init_jwt


class RegexConverter(BaseConverter):
    """路由正则转化的类"""

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask("Mylog")
CORS(app, supports_credentials=True)
app.url_map.converters['regex'] = RegexConverter
app.config.from_pyfile("settings.py")
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# 日志配置
logger = Logger()
logger.init_app(app)

# 缓存
cache = Cache(app)

# 数据库配置
db = SQLAlchemy(app)
mg = Migrate(app, db)

# csrf保护
csrf = CSRFProtect()
csrf.init_app(app)

# moment插件
moment = Moment(app)

# 响应压缩css，js以及html
Minify(app=app, html=True, js=True, cssless=True)

# 邮件
mail = Mail(app)
# scss插件
if app.config.get('SCSS_ENABLED', False):
    Scss(app)

jwt = init_jwt(app)


from Mylog.filter import *
from Mylog.models import *
from Mylog.inject import *
from Mylog.view import *
from Mylog.api import *

# 自定义命令
from Mylog.commands import init
