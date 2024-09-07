# -*- coding: utf-8 -*-
"""
    @File: pageViewerService.py
    @Author:Wang Shihan
    @Date:2024/7/19
    @Description:
"""
import datetime
from datetime import datetime
from sqlalchemy import extract

from Mylog.store.iService import ServerBase
from Mylog.models import PageViewer
from Mylog.util.tool import short_uuid, get_day_list, extract_device


class PageViewerService(ServerBase):
    def create(self, file, data: dict):
        pass

    def get_all(self) -> list:
        pass

    def get_by_many(self, *args, **kwargs):
        pass

    def get_one(self, id: int):
        pass

    def update(self, data: dict) -> bool:
        pass

    def cover(self, id, file) -> bool:
        pass

    def delete(self, id):
        pass

    def get_by_date(self, date=None, scope='month'):
        if isinstance(date, str):
            now = datetime.fromisoformat(date)
        elif isinstance(date, datetime):
            now = date
        else:
            now = datetime.now()

        if scope == 'year':
            return (
                PageViewer.query.filter(
                    extract('year', PageViewer.enter) == now.year,
                )
                .order_by(PageViewer.enter.desc())
                .all()
            )
        elif scope == 'day':
            return (
                PageViewer.query.filter(
                    extract('year', PageViewer.enter) == now.year,
                    extract('month', PageViewer.enter) == now.month,
                    extract('day', PageViewer.enter) == now.day,
                )
                .order_by(PageViewer.enter.desc())
                .all()
            )
        else:
            return (
                PageViewer.query.filter(
                    extract('year', PageViewer.enter) == now.year,
                    extract('month', PageViewer.enter) == now.month,
                )
                .order_by(PageViewer.enter.desc())
                .all()
            )

    def stat_history(self, dt: str = None):
        if dt is None:
            now = datetime.now()
        else:
            now = datetime.fromisoformat(dt)
        visitors = self.get_by_date(now)
        days = get_day_list(now.year, now.month)
        visit_dic = dict.fromkeys(days, 0)
        for v in visitors:
            str_time = v.enter.strftime('%Y-%m-%d')
            visit_dic[str_time] += 1

        return {"labels": list(visit_dic.keys()), "values": list(visit_dic.values())}

    def stat_domestic(self, dt: str):
        visitors = self.get_by_date(dt)
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
        return [{"name": k, "value": json_dic[k]} for k in json_dic.keys()]

    def stat_records(self, date: str):
        def detect_datetime(x):
            return str(x.time())[0:7] if x else '无'

        def detect_user(x):
            bots = [
                {
                    'user': 'RSS',
                    'keyword': ['Fresh', 'rss', 'RSS', 'Feedly', 'ReadYou', 'Reader'],
                },
                {'user': 'bot', 'keyword': ['bot', 'spider', 'company']},
            ]
            for b in bots:
                for k in b['keyword']:
                    if k in x:
                        return 'bot/spider'
            return extract_device(x)

        visitors = self.get_by_date(date, scope='day')
        return [
            {
                "ip": v.ip,
                "province": v.province,
                'city': v.city,
                'device': v.device,
                'referer': v.referer,
                "enter": detect_datetime(v.enter),
                "leave": detect_datetime(v.leave),
                "page": v.page,
                'stay': round(v.stay, 2),
                'user': detect_user(v.ua),
            }
            for v in visitors
        ]
