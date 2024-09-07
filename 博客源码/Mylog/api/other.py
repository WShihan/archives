# -*- coding: utf-8 -*-
"""
    @file: mylog.py
    @Author:Wang Shihan
    @Date:2023/7/31
    @Description: the apis file of blog
"""
import re
from datetime import datetime
from flask import request
from flask import redirect
from flask_jwt_extended import jwt_required

from Mylog import app, csrf
from Mylog.store.blog import BlogService
from Mylog.store.pageViewer import PageViewerService
from Mylog.models import BlogType, PageViewer
from Mylog.hooks import varify_token, universal_api
from Mylog.models import User, Blog
from Mylog.util.tool import extract_ip, extract_device, IPChecker, show_except

service = BlogService()
ppvService = PageViewerService()


@app.route('/mylog/whisper/create/bot', methods=['POST'])
@csrf.exempt
def whisper_create_bot():
    try:
        form = request.form
        user = form.get('user')
        password = form.get('password')
        content = form.get('content')
        time = form.get('time', datetime.now())

        user = User.query.filter(User.name == user, User.password == password).first()
        if user is None or content == '':
            raise ValueError()

        service.create(
            {
                'title': '日记',
                'type': BlogType.DIARY,
                'body': content,
                'intro': content[:50],
                'category': '日记',
                'visible': False,
                'time': time,
            }
        )
        return redirect('/whisper')
    except Exception as e:
        return show_except(msg=str(e), code=500)


@app.route('/mylog/ppv/collect', methods=['POST'])
@csrf.exempt
@universal_api
def page_view():
    data = request.json
    vid = data.get('vid')
    uid = data.get('uid')
    sid = data.get('sid')
    ip = extract_ip(request)
    ua = request.user_agent.string
    device = extract_device(request.user_agent.string)
    ip_info = IPChecker(app.config['GEO_DECODE_AK']).check(ip)
    url = data.get('url')
    if not uid or not vid:
        raise ValueError('uid or vid is required!')

    # 匹配博客访问统计
    blog_match_result = re.search(r'/blog/(\d{8})', url)
    if not blog_match_result:
        blog_match_result = re.search(r'all-about-gis/issue-(\d+)', url)
    if blog_match_result is not None:
        blog_id = blog_match_result.group(1)
        blog = Blog.query.filter(Blog.id == blog_id).first()
        if blog:
            blog.visited += 1
            service.save2db(blog)

    pv = PageViewer.query.filter(PageViewer.vid == vid, PageViewer.url == url).first()
    if pv:
        pv.leave = datetime.now()
        pv.stay = pv.leave.timestamp() - pv.enter.timestamp()
    else:
        pv = PageViewer(
            vid=vid,
            ip=ip,
            uid=uid,
            sid=sid,
            sw=data.get('sw'),
            device=device,
            ua=ua,
            province=ip_info.province,
            city=ip_info.city,
            lon=ip_info.lon,
            lat=ip_info.lat,
            page=data.get('tt'),
            tz=data.get('tz'),
            lang=data.get('lang'),
            referer=data.get('ref'),
            url=url,
        )
    service.save2db(pv)
    return None


@app.route('/mylog/ppv/history', methods=['GET'])
@jwt_required()
@varify_token
@universal_api
def ppv_history():
    dt = request.args.get('date')
    return ppvService.stat_history(dt)


@app.route('/mylog/ppv/domestic', methods=['GET'])
@jwt_required()
@varify_token
@universal_api
def ppv_domestic():
    date = request.args.get('date')
    return ppvService.stat_domestic(date)


@app.route('/mylog/ppv/records', methods=['GET'])
@jwt_required()
@varify_token
@universal_api
def ppv_records():
    date = request.args.get('date')
    return ppvService.stat_records(date)
