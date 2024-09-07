# -*- coding: utf-8 -*-
"""
    @file: commentService.py
    @Author:Wang Shihan
    @Date:2023/9/16
    @Description:
"""
from datetime import datetime
from flask_mail import Message
from flask import request, render_template
from sqlalchemy import desc, or_

from Mylog.store.iService import ServerBase
from Mylog.models import Comment, Blog
from Mylog.util.tool import short_uuid
from Mylog import mail, app
from Mylog.util.tool import IPChecker, extract_device, extract_ip


class CommentService(ServerBase):
    def create(self, data: dict):
        blog_id = data['blogid']
        reply_id = data['replyid']
        comment = data['comment']
        email = data['email']
        email = email if email != '' else None
        site = data['site']
        reply_id = reply_id if reply_id != '' else None
        nickname = data.get('nickname')
        nickname = nickname if nickname != '' else "匿名"
        if blog_id == "" or comment == "":
            raise ValueError('请填写信息！')

        blog = Blog.query.filter(Blog.id == blog_id).first()
        ip = extract_ip(request)
        ip_info = IPChecker(app.config['GEO_DECODE_AK']).check(ip)
        cmt = Comment(
            id=short_uuid(),
            parent_id=reply_id,
            ip=ip,
            email=email,
            site=site,
            province=ip_info.province,
            city=ip_info.city,
            device=extract_device(request.user_agent.string),
            body=comment,
            blogid=blog_id,
            nickname=nickname,
            audit=True,
            time=datetime.now(),
        )
        self.save2db(cmt)

        # 发送邮件提醒
        try:
            parent_cmt = Comment.query.filter(Comment.id == reply_id).first()
            # 通知父评论
            if parent_cmt:
                if parent_cmt.email is not None or parent_cmt.email != '':
                    accepts = []
                    accepts.append(parent_cmt.email)
                    subject = "「wsh233.cn」评论回复提醒"
                    message = Message(subject=subject, recipients=accepts, body=comment)
                    message.html = render_template(
                        'email.html',
                        msg=comment,
                        blog=blog,
                        reply=parent_cmt,
                        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    mail.send(message)

            # 通知admin
            subject = "「wsh233.cn」评论通知"
            message = Message(
                subject=subject, recipients=['3443327820@qq.com'], body=comment
            )
            message.html = render_template(
                'notify.html',
                blog=blog,
                cmt=cmt,
                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            mail.send(message)

        except Exception as e:
            app.logger.error(f'邮件通知错误：{str(e)}')

    def get_all(self) -> list:
        cmts: list = Comment.query.all()
        return [self.extract_attr(cmt) for cmt in cmts]

    def get_by_many(
        self,
        args: dict,
    ):
        page = args.get('page', 0)
        limit = args.get('limit', 10)
        keyword = args.get('keyword', '')
        query = Comment.query.filter(
            or_(
                Comment.body.like(f'%{keyword}%'),
                Comment.nickname.like(f'%{keyword}%'),
            )
        ).order_by(desc(Comment.time))
        total = query.count()
        cmts = query.offset(page * limit).limit(limit)
        return {'total': total, 'rows': [self.extract_attr(c) for c in cmts]}

    def get_one(self, *args, **kwargs) -> dict:
        pass

    def update(self, *args, **kwargs) -> bool:
        pass

    def audit(self, id: str) -> bool:
        cmt = Comment.query.filter(Comment.id == id).first()
        if cmt:
            cmt.audit = not cmt.audit
            self.save2db(cmt)
            return True
        else:
            return False

    def delete(self, id: str) -> bool:
        cmt = Comment.query.filter(Comment.id == id).first()
        if cmt:
            self.delete_from_db(cmt)
            return True
        else:
            return False
