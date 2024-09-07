# -*- coding: utf-8 -*-
"""
    @file: blogService.py
    @Author:Wang Shihan
    @Date:2023/7/31
    @Description: blog service
"""
from datetime import datetime
from typing import List
from sqlalchemy import desc, extract, or_
from flask_jwt_extended import create_access_token

from Mylog.util.tool import get_day_list, validate_datetime
from Mylog.store.iService import ServerBase
from Mylog.models import Blog, User, Viewer, BlogType
from Mylog.util.tool import short_uuid, IP
from Mylog import cache


class BlogService(ServerBase):
    def create(self, data: dict):
        json_data = data
        title = json_data['title']
        type = json_data.get('type', 0)
        body = json_data['body']
        category = json_data.get('category', '杂')
        intro = json_data.get('intro')
        time = json_data.get('time')
        time = datetime.now() if time is None else validate_datetime(time)
        visible = json_data.get('visible')
        note = json_data.get('note')
        if int(type) == BlogType.PUBLICATION:
            id = f'issue-{self.get_visible_blog_count(blog_type=BlogType.PUBLICATION) + 1}'
        else:
            id = short_uuid()

        blog = Blog(
            id=id,
            type=type,
            title=title,
            body=body,
            category=category,
            time=time,
            intro=intro,
            visited=0,
            visible=visible,
            note=note,
        )
        self.save2db(blog)
        self.update_cache()

        return True

    def get_by_many(self, args: dict):
        blog_type = args.get('type', 0)
        page = args.get('page', 0)
        limit = args.get('limit', 10)
        publish = args.get('publish', True)
        keyword = args.get('keyword', '')
        query = (
            Blog.query.filter(Blog.publish == publish)
            .filter(
                or_(Blog.title.like(f'%{keyword}%'), Blog.category.like(f'%{keyword}%'))
            )
            .filter(Blog.type == blog_type)
            .order_by(desc(Blog.time))
        )
        total = query.count()
        blogs = query.offset(page * limit).limit(limit)
        return {'total': total, 'rows': [self.extract_attr(b) for b in blogs]}

    def get_visible_blog(self, blog_type: int) -> List:
        return (
            Blog.query.filter(
                Blog.type == blog_type, Blog.publish == True, Blog.visible == True
            )
            .order_by(Blog.time.desc())
            .all()
        )

    def get_visible_blog_count(self, blog_type: int) -> int:
        return (
            Blog.query.filter(
                Blog.type == blog_type, Blog.publish == True, Blog.visible == True
            )
            .order_by(Blog.time.desc())
            .count()
        )

    @cache.cached('blogs')
    def get_all(self, is_publish=True) -> list:
        blogs = Blog.query.filter(Blog.publish == is_publish).order_by(desc(Blog.time))
        return [self.extract_attr(b) for b in blogs]

    def get_visible_blogs(self) -> List[Blog]:
        blogs = self.get_all()
        return [b for b in blogs if b.visible and b.publish]

    def get_one(self, id) -> dict:
        b = Blog.query.filter(Blog.id == id).first()
        if b:
            self.save2db(b)
            return {
                'id': b.id,
                "title": b.title,
                "body": b.body,
                "type": b.type,
                "category": b.category,
                'intro': b.intro,
                'time': b.time.strftime('%Y-%m-%d'),
            }
        else:
            return {}

    def delete(self, id) -> bool:
        blog = Blog.query.filter(Blog.id == id).first()
        if blog:
            self.delete_from_db(blog)
            self.update_cache()
            return True
        else:
            return False

    def update(self, data: dict):
        """
        :param data: {id, body, title, intro,visible, category}
        :return:
        """
        json_data = data
        id = json_data['id']
        update_blog = Blog.query.get(id)
        for k, v in data.items():
            # 如果修改的是内容，更新修改时间
            try:
                setattr(update_blog, k, v)
                self.save2db(update_blog)
            except Exception as e:
                continue

        self.update_cache()
        return True

    def publish(self, id) -> bool:
        blog = Blog.query.filter(Blog.id == id).first()
        if blog:
            blog.publish = True
            self.save2db(blog)
            self.update_cache()
            return True
        else:
            return False

    def authenticate(self, data: dict):
        user_name = data['username']
        password = data['password']
        user = User.query.filter(
            User.name == user_name, User.password == password
        ).first()
        if user:
            token = create_access_token(identity=user_name)
            return {'username': user_name, 'token': f'Bearer {token}'}
        else:
            raise ValueError('错误,用户名或密码错误')

    def filter_visitors(self, date=None, year=False, month=False, day=False):
        query = Viewer.query
        query.filter()
        date = datetime.now() if date is None else date
        if year and not (month and day):
            query = query.filter(extract('year', Viewer.latest) == date.year)
        if month and not day:
            query = query.filter(
                extract('year', Viewer.latest) == date.year,
                extract('month', Viewer.latest) == date.month,
            )
        if day:
            query = query.filter(
                extract('year', Viewer.latest) == date.year,
                extract('month', Viewer.latest) == date.month,
                extract('day', Viewer.latest) == date.day,
            )

        return query.order_by(Viewer.latest.desc()).all()

    def stasis(self, chart_type: str, args):
        stasis_type = chart_type
        date = args.get('date')
        if date is None:
            visitors = self.filter_visitors()
            now = datetime.now()
        else:
            now = datetime.strptime(date, '%Y-%m-%d')
            visitors = self.filter_visitors(now, month=True)
        if stasis_type == 'history':
            days = get_day_list(now.year, now.month)
            visit_dic = dict.fromkeys(days, 0)
            for v in visitors:
                str_time = v.latest.strftime('%Y-%m-%d')
                if str_time not in visit_dic.keys():
                    visit_dic[str_time] = 1
                else:
                    visit_dic[str_time] += 1
            response_data = {
                "labels": list(visit_dic.keys()),
                "values": list(visit_dic.values()),
            }
        elif stasis_type == 'ipRank':
            raise ValueError('无信息')
        elif stasis_type == 'category':
            blogs = Blog.query.all()
            json_dic = dict()
            for b in blogs:
                if b.category not in json_dic.keys():
                    json_dic[b.category] = 1
                else:
                    json_dic[b.category] += 1
            response_data = [{"name": j, "value": json_dic[j]} for j in json_dic]
        elif stasis_type == 'blogView':
            blogs = self.get_visible_blog(BlogType.BLOG) + self.get_visible_blog(
                BlogType.PUBLICATION
            )
            response_data = {
                "labels": [b.title for b in blogs],
                "values": [b.visited for b in blogs],
            }
        elif stasis_type == 'province':
            json_dic = dict()
            for v in visitors:
                if v.province is None or v.province == '':
                    continue
                prov = v.province.strip("省市")
                if prov == "" or prov is None:
                    continue
                if prov not in json_dic.keys():
                    json_dic[prov] = 1
                else:
                    json_dic[prov] += 1
            response_data = [{"name": k, "value": json_dic[k]} for k in json_dic.keys()]
        elif stasis_type == 'today':
            viewers = self.filter_visitors(now, day=True)
            response_data = [
                {
                    "ip": v.ip,
                    "province": v.province,
                    'city': v.city,
                    'device': v.device,
                    'referer': v.referer,
                    "time": str(v.latest.time())[0:5],
                    "page": v.page,
                    'ua': v.ua,
                }
                for v in viewers
            ]
        elif stasis_type == 'distribution':
            visitors = self.filter_visitors(now, day=True)
            ips = [
                IP(
                    ip=v.ip,
                    country=v.country,
                    province=v.province,
                    city=v.city,
                    lat=v.lat,
                    lon=v.lon,
                ).par2dic()
                for v in visitors
                if v.lon != 'None' and v.lat != 'None'
            ]
            response_data = ips
        else:
            raise ValueError()
        return response_data

    def save2db(self, obj):
        super().save2db(obj)
        self.update_cache()

    def update_cache(self):
        cache.delete('blogs')
        cache.delete('whisper')
        cache.delete('feed')
        cache.delete('index')
