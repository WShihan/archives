# -*- coding: utf-8 -*-
"""
@Date: 2021/10/2 23:23
@Author:Wang Shihan
@File: tool.py
@Software: PyCharm
"""
from user_agents import parse
import json
from requests import get
from calendar import monthrange
from datetime import datetime
from flask import Request, render_template
import uuid
import random
from Mylog.response import ApiResponse
from Mylog import app


def log_except(e: Exception):
    app.logger.error(str(e))
    return ApiResponse(str(e)).failed


def show_except(msg: str = '404', title: str = '异常 (-_-)', error=None, code=404):
    if error:
        app.logger.error(f'error\t{str(error)}')
        app.logger.error(f'msg\t{str(error)}')
    return render_template('status.html', msg=msg, title=title, nav='错误页面'), code


def parse_token(cookies: str) -> str:
    """
    解析token
    :param cookies: cookies
    :return: str or None
    """
    token = None
    if cookies is None:
        return token
    for c in cookies.split(";"):
        if 'token' in c:
            token = c
            break
    return token


class IP:
    def __init__(self, ip, country=None, province=None, city=None, lon=None, lat=None):
        self.country = country
        self.province = province
        self.city = city
        self.lon = lon
        self.lat = lat
        self.ip = ip

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"""IP Object ip:{self.ip}"""

    def par2dic(self):
        return {
            'ip': self.ip,
            'country': self.country,
            'province': self.province,
            'city': self.city,
            'lon': self.lon,
            'lat': self.lat,
        }


class IPChecker:
    """IP地址查询类"""

    def __init__(self, ak: str):
        self.check_url = 'https://api.map.baidu.com/location/ip?'
        self.params = {'ak': ak, 'ip': '', 'coor': 'bd09ll'}
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
        }

    def get_baidu(self, ip: str) -> IP:
        self.params['ip'] = ip
        res = get(
            url=self.check_url, params=self.params, timeout=5, headers=self.headers
        )
        if res.status_code == 200:
            res.encoding = res.apparent_encoding
            ip_info = json.loads(res.text)
            if ip_info['status'] == 0:
                address = ip_info['content']['address_detail']
                province = address['province']
                city = address['city']
                point = ip_info['content']['point']
                lon = point.get('x')
                lat = point.get('y')
                return IP(
                    ip, country="CN", province=province, city=city, lon=lon, lat=lat
                )
            else:
                return None
        else:
            return None

    def get_ip_location(self, ip: str) -> IP:
        resp = get(
            f'https://api.ip2location.io/?key=35DE45B78E3A5C10B042867B158EE75E&ip={ip}',
            timeout=5,
            headers=self.headers,
        )
        data = resp.json()
        country = data.get('country_name')
        province = data.get('region_name')
        city = data.get('city_name')
        lon = data.get('longitude')
        lat = data.get('latitude')
        return IP(ip, country=country, province=province, city=city, lon=lon, lat=lat)

    def check(self, ip) -> IP:
        try:
            resp = self.get_baidu(ip)
            if resp is None:
                return self.get_ip_location(ip)
            else:
                return resp
        except Exception as e:
            print(f"错误：{str(e)}")


class Status:
    """
    状态类
    """

    def __init__(self, title="Page Not Found", code=404, msg="页面未找到"):
        self.__title = title
        self.__code = code
        self.__msg = msg

    @property
    def body(self):
        return {"title": self.__title, "code": self.__code, "msg": self.__msg}

    @property
    def code(self):
        return self.__code


# 解析ip，使用nginx转发后，无法以常规方式获取客户端真实ip
def extract_ip(req: Request) -> str:
    forwarded_ip = req.headers.get('x-forwarded-for')
    ips = [req.remote_addr] if forwarded_ip is None else forwarded_ip.split(',')
    ip = "127.0.0.1"
    for item in ips:
        if not item.endswith("0.0.1"):
            ip = item
    return ip


def extract_device(ua: str) -> str:
    """
    提取设备
    :param ua:
    :return:
    """
    agent = parse(ua)
    return agent.os.family


def short_uuid(num=8) -> str:
    """
    获取八位随机uid
    :return:
    """
    uid = str(uuid.uuid4().int)
    head = random.randint(0, 30)
    id = uid[head : head + num]
    return id.zfill(num)


class SiteMap:
    def __init__(self):
        self.__header = '''<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>'''
        self.__urls = []

    def add_url(self, url: dict):
        dt = datetime.utcnow()
        self.__urls.append(
            f"""
        <url>
            <loc>{url['loc']}</loc>
            <lastmod>{url.get('lastmod', dt.strftime('%Y-%m-%d'))}</lastmod>
            <priority>{url.get('priority', 1)}</priority>
            <changefreq>{url.get('changefreq', 'monthly')}</changefreq>
        </url>"""
        )

    def to_string(self):
        return self.__header % ''.join(self.__urls)


def get_day_list(year, month):
    """
    返回年份、月份内包含的日列表
    :param year:
    :param month:
    :return:
    """
    day_lis = []
    for day in range(monthrange(year, 12)[1] + 1)[1:]:
        day_lis.append('%s-%s-%s' % (year, '%02d' % month, '%02d' % (day)))
    return day_lis


def validate_datetime(date_string: str) -> datetime:
    if date_string is None:
        return None
    fmt_patterm = [
        'YYYY-MM-DDTHH:MM:SS±HH:MM',
        'YYYY-MM-DD',
        'YYYY-MM-DDTHH:MM:SS',
        'MM/DD/YYYY HH:MM AM/PM',
        'MM/DD/YYYY',
        'MM-DD-YYYY',
        'DD/MM/YYYY HH:MM',
        'DD/MM/YYYY',
        'DD-MM-YYYY',
    ]
    dt = None
    for fmt in fmt_patterm:
        try:
            dt = datetime.strptime(date_string, fmt)
            break
        except ValueError:
            pass
    return dt

    try:
        # 尝试将字符串解析为 datetime 对象
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
