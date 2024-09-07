# -*- coding: utf-8 -*-
"""
    @file: response.py
    @Author:Wang Shihan
    @Date:2023/8/16
    @Description: the obj response of api
"""
from flask import jsonify
from functools import wraps
from Mylog import app


class ApiResponse:
    def __init__(self, msg: str = 'success', data=None, code=200) -> None:
        self.__status = True
        self.__msg = msg
        self.__data = data
        self.__code = code

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, msg):
        self.__msg = msg

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def success(self):
        return self.jsonify(True)

    @property
    def failed(self):
        return self.jsonify(False)

    def jsonify(self, status) -> jsonify:
        return jsonify(
            {
                'status': status,
                'msg': self.__msg,
                'data': self.data,
                'code': self.__code,
            }
        )


def universal_api(func):
    """
    统一接口返回数据类型
    """

    def log_except(e: Exception):
        app.logger.error(str(e))
        return ApiResponse(str(e)).failed

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res_data = func(*args, **kwargs)
            return ApiResponse(data=res_data).success
        except Exception as e:
            return log_except(e)

    return wrapper
