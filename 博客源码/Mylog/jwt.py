# -*- coding: utf-8 -*-
"""
    @File: jwt.py
    @Author:Wang Shihan
    @Date:2024/8/2
    @Description:
"""
from flask import Flask
from flask_jwt_extended import JWTManager


def init_jwt(app: Flask) -> JWTManager:
    return JWTManager(app)
