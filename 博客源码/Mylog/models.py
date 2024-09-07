# -*- coding: utf-8 -*-
"""
    @Date:  2022-05-26 
    @Author:Wang Shihan
    @Desc:模型文件
    数据库更新：
    1. >> flask db init
    2.>> flask db migrate -m "add ModelName newColumnName"
    3.>> flask db upgrade
"""
from datetime import datetime
from Mylog import db


class Viewer(db.Model):
    """
    访问
    """

    __tablename__ = "Viewer"
    id = db.Column(db.Integer, primary_key=True)
    # ip
    ip = db.Column(db.String(50))
    # token
    token = db.Column(db.String(255))
    # 国家/地区
    country = db.Column(db.String(255))
    # 省份
    province = db.Column(db.String(255))
    # 城市
    city = db.Column(db.String(255))
    # 页面
    page = db.Column(db.String(255))
    # 最近访问
    latest = db.Column(db.DateTime, default=datetime.now, index=True)
    # 次数
    count = db.Column(db.Integer)
    # 设备
    device = db.Column(db.String(255))
    # 用户头user-agent
    ua = db.Column(db.Text)
    # 来源
    referer = db.Column(db.String(255))
    # 来源经度
    lon = db.Column(db.Float)
    # 来源纬度
    lat = db.Column(db.Float)
    # 备注
    note = db.Column(db.String(255))


class PageViewer(db.Model):
    """
    页面访问用户
    """

    __tablename__ = "PageViewer"
    id = db.Column(db.Integer, primary_key=True)
    # 单次访问id
    vid = db.Column(db.String(20), nullable=False)
    # 访问者id
    uid = db.Column(db.String(20), nullable=False)
    # 会话id
    sid = db.Column(db.String(20), nullable=False)
    # ip
    ip = db.Column(db.String(50))
    # 进入时间戳
    enter = db.Column(db.DateTime, default=datetime.now)
    # 离开时间戳
    leave = db.Column(db.DateTime)
    # 住存时间
    stay = db.Column(db.Float, default=0)
    # screen width
    sw = db.Column(db.Integer, default=0)
    # time zone
    tz = db.Column(db.Integer, default=0)
    # url
    url = db.Column(db.String(255))
    # 国家/地区
    country = db.Column(db.String(255))
    # 省份
    province = db.Column(db.String(255))
    # 城市
    city = db.Column(db.String(255))
    # 页面
    page = db.Column(db.String(255))
    # 设备
    device = db.Column(db.String(255))
    # 语言
    lang = db.Column(db.String(20))
    # 用户头user-agent
    ua = db.Column(db.Text)
    # 来源
    referer = db.Column(db.String(255))
    # 来源经度
    lon = db.Column(db.Float)
    # 来源纬度
    lat = db.Column(db.Float)
    # 备注
    note = db.Column(db.String(255))


class User(db.Model):
    """
    mylog 用户
    """

    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    name = db.Column(db.String(20), nullable=False)
    # 密码
    password = db.Column(db.String(16), nullable=False)
    # token
    token = db.Column(db.String(250))
    # token失效时间
    expire = db.Column(db.DateTime, default=datetime.now, nullable=False)
    # 首页markdown
    index = db.Column(db.Text)
    # 关于页面markdown
    about = db.Column(db.Text)
    # 备注
    note = db.Column(db.String(50))
    # 所属博客
    blogs = db.relationship("Blog")


class Cover(db.Model):
    """
    封面
    """

    __tablename__ = 'Cover'
    id = db.Column(db.String(255), primary_key=True)
    # 封面链接
    url = db.Column(db.String(255))
    # 封面文字
    saying = db.Column(db.String(1000))
    # 图片类型
    img_type = db.Column(db.String(12))
    # 日期时间
    time = db.Column(db.DateTime, default=datetime.now, index=True)


class BlogType:
    BLOG = 0
    DIARY = 1
    PUBLICATION = 2


class Blog(db.Model):
    """
    博文
    """

    __tablename__ = "Blog"
    id = db.Column(db.String(200), primary_key=True)
    # 类型 0:博文,1:日记,2:周刊
    type = db.Column(db.Integer, default=0, nullable=True)
    # 标题
    title = db.Column(db.String(200))
    # 简介
    intro = db.Column(db.Text)
    # 内容
    body = db.Column(db.Text)
    # 创建时间
    time = db.Column(db.DateTime, default=datetime.now, index=True)
    # 是否发布
    publish = db.Column(db.Boolean, default=True)
    # 更新时间
    update = db.Column(db.DateTime, index=True, default=None)
    # 访问数
    visited = db.Column(db.Integer, default=0)
    # 是否置顶
    pin = db.Column(db.Boolean, default=False)
    # 是否原创
    original = db.Column(db.Boolean, default=True)
    # 分类
    category = db.Column(db.String(20))
    # 是否允许rss可见
    visible = db.Column(db.Boolean, default=False)
    # 是否评论
    commentable = db.Column(db.Boolean, default=True)
    # 评论关系
    comments = db.relationship("Comment")
    # 备注
    note = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('User.id'))


class Comment(db.Model):
    """
    评论
    """

    __tablename__ = "Comment"
    id = db.Column(db.String(200), primary_key=True)
    # ip
    ip = db.Column(db.String(200))
    # 内容体
    body = db.Column(db.Text)
    # 昵称
    nickname = db.Column(db.String(255))
    # 邮箱
    email = db.Column(db.String(50))
    # 站点
    site = db.Column(db.String(50))
    # 省份
    province = db.Column(db.String(200))
    # 城市
    city = db.Column(db.String(200))
    # 设备
    device = db.Column(db.String(50))
    # 审核
    audit = db.Column(db.Boolean, default=False)
    # 时间
    time = db.Column(db.DateTime, default=datetime.now, index=True)
    # 父评论
    parent = db.relationship('Comment', remote_side=[id])
    # 父评论id, 自引用关系
    parent_id = db.Column(db.String(200), db.ForeignKey('Comment.id'))
    # 博客id
    blogid = db.Column(db.String(255), db.ForeignKey('Blog.id'))
