# -*- coding: utf-8 -*-
"""
    @file: mylog.py
    @Author:Wang Shihan
    @Date:2023/7/31
    @Description: the apis file of user
"""
from flask import request
from flask_jwt_extended import jwt_required

from Mylog.models import User
from Mylog.hooks import varify_token, universal_api
from Mylog import app, csrf
from Mylog.store.blog import BlogService


service = BlogService()


@app.route('/mylog/user/get/<name>', methods=['GET'])
@jwt_required()
@varify_token
@universal_api
def user_get(name: str):
    user = User.query.filter(User.name == name).first()
    return {
        'id': user.id,
        'name': user.name,
        'password': user.password,
        'about': user.about,
        'index': user.index,
        'note': user.note,
    }


@app.route('/mylog/user/update', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def user_update():
    data = request.json
    id = data['id']
    user = User.query.filter(User.id == id).first()
    if user is None:
        raise ValueError()
    for k, v in data.items():
        setattr(user, k, v)
    service.save2db(user)


@app.route('/mylog/user/login', methods=['POST'])
@csrf.exempt
@universal_api
def authentication():
    data = service.authenticate(request.json)
    return data
