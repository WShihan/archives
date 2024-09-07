# -*- coding: utf-8 -*-
"""
    @File: hooks.py
    @Author:Wang Shihan
    @Date:2024/5/13
    @Description: 钩子装饰器
"""
from flask import request, make_response
import time
from hashlib import md5
from functools import wraps
from flask_jwt_extended import get_jwt_identity

from Mylog.models import User
from Mylog.response import ApiResponse
from Mylog.util.tool import parse_token, short_uuid, log_except


def universal_api(func):
    """统一接口返回数据类型

    Args:
        func (Function view): 视图函数

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res_data = func(*args, **kwargs)
            return ApiResponse(data=res_data).success
        except Exception as e:
            return log_except(e)

    return wrapper


def varify_token(func):
    """统一验证jwt token是否有效钩子

    Args:
        func (Function view): 视图函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        identify = get_jwt_identity()
        user = User.query.filter(User.name == identify).first()
        if user is None:
            return ApiResponse(msg="Forbidden", code=403).failed
        else:
            return func(*args, **kwargs)

    return wrapper


# 页面请求守卫，处理token
def page_gard(func):
    """_summary_

    Args:
        func (Function view): 页面访问守卫路由钩子

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        token = parse_token(request.headers.get('Cookie'))
        md = md5()
        resp = make_response(func(*args, **kwargs))
        if not token:
            ip = request.remote_addr
            ua = request.user_agent
            md.update((ip + str(ua) + str(time.time())).encode('utf-8'))
            token = md.hexdigest()
            resp.set_cookie(
                key='token',
                value=token,
                max_age=31536000,
                secure=True,
                httponly=True,
                samesite='Strict',
            )
            resp.set_cookie(
                key='uid',
                value=short_uuid(12),
                max_age=60 * 60 * 24 * 365,
                secure=False,
                httponly=False,
                samesite='Strict',
            )
        return resp

    return wrapper
