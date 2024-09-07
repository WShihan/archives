# -*- coding: utf-8 -*-
"""
    @file: mylog.py
    @Author:Wang Shihan
    @Date:2023/7/31
    @Description: the apis file of moment
"""
from flask import request
from flask_jwt_extended import jwt_required

from Mylog import app, csrf
from Mylog.store.cover import CoverService
from Mylog.hooks import varify_token, universal_api
from Mylog.util.cos import COS

cos = COS(app.config['COS_URL'])
cover_service = CoverService()


@app.route('/mylog/moment/create', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def one_create():
    return cover_service.create(request.files.get('file'), request.form)


@app.route('/mylog/moment/all')
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def one_all():
    return cover_service.get_all()


@app.route('/mylog/moment/many', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def moment_many():
    args = request.json
    return cover_service.get_by_many(args)


@app.route('/mylog/moment/get/<id>', methods=['GET'])
@csrf.exempt
@universal_api
def one_single(id):
    return cover_service.get_one(int(id))


@app.route('/mylog/moment/update', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def one_edit():
    return cover_service.update(request.json)


@app.route('/mylog/moment/delete/<id>', methods=['GET'])
@jwt_required()
@varify_token
@universal_api
def one_del(id):
    return cover_service.delete(id)


@app.route('/mylog/moment/cover', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def one_cover():
    return cover_service.cover(request.form.get('id'), request.files.get('file'))
