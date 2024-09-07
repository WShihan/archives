# -*- coding: utf-8 -*-
"""
    @file: mylog.py
    @Author:Wang Shihan
    @Date:2023/7/31
    @Description: the apis file of blog
"""

from flask import request
from flask_jwt_extended import jwt_required

from Mylog import app, csrf
from Mylog.store.blog import BlogService
from Mylog.filter import md2html
from Mylog.hooks import varify_token, universal_api

service = BlogService()


@app.route('/mylog/blog/all', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def blog_all():
    data = service.get_all(is_publish=True)
    return data


@app.route('/mylog/blog/many', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def blog_many():
    args = request.json
    return service.get_by_many(args)


@app.route('/mylog/blog/get/<id>')
@jwt_required()
@varify_token
@universal_api
def blog_single(id):
    return service.get_one(id)


@app.route('/mylog/blog/create', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def blog_create():
    service.create(request.json)


@app.route('/mylog/blog/update', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def blog_update():
    return service.update(request.json)


@app.route('/mylog/blog/delete/<id>')
@jwt_required()
@varify_token
@universal_api
def blog_del(id):
    return service.delete(id)


@app.route('/mylog/blog/stasis/<string:chart_type>', methods=['GET', 'POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def blog_stasis(chart_type):
    args = request.args
    return service.stasis(chart_type, args)


@app.route('/mylog/blog/markdown2html', methods=['POST'])
@csrf.exempt
@universal_api
def convert_md():
    md = request.json.get('body', None)
    if md:
        return md2html(md)
    else:
        raise ValueError('无markdown文本')
