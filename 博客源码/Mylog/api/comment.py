# -*- coding: utf-8 -*-
"""
    @file: mylog.py
    @Author:Wang Shihan
    @Date:2023/7/31
    @Description: the apis file of comment
"""

from flask import request
from flask_jwt_extended import jwt_required
from Mylog import app, csrf
from Mylog.hooks import varify_token, universal_api
from Mylog.store.comment import CommentService

comment_service = CommentService()


@app.route('/mylog/comment/create', methods=["POST"])
@csrf.exempt
@universal_api
def comment_create():
    data = request.json
    return comment_service.create(data)


@app.route('/mylog/comment/all', methods=['GET', 'POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def comment_all():
    return comment_service.get_all()


@app.route('/mylog/comment/many', methods=['POST'])
@csrf.exempt
@jwt_required()
@varify_token
@universal_api
def comment_many():
    args = request.json
    return comment_service.get_by_many(args)


@app.route('/mylog/comment/delete/<id>')
@jwt_required()
@varify_token
@universal_api
def comment_delete(id: str):
    return comment_service.delete(id)


@app.route('/mylog/comment/audit/<id>')
@jwt_required()
@varify_token
@universal_api
def comment_audit(id: str):
    return comment_service.audit(id)
