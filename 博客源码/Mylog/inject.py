# -*- coding: utf-8 -*-
"""
    @File: inject.py
    @Author:Wang Shihan
    @Date:2024/5/13
    @Description:
"""
from datetime import datetime
from flask import request
from Mylog import app


@app.context_processor
def inject_custom_context():
    """
    注册所有全局内置环境变量，所有模板均可使用
    """
    # 如果显示模式没有设置，请求时根据时间自动设置
    cookie = request.cookies
    mode = cookie.get('view-mode', 'normalmode')

    inject_dict = {
        'app_copyright_year_start': "2020",
        'app_copyright_year_end': datetime.now().year,
        'track': app.config.get('TRACK', True),
    }

    return inject_dict
