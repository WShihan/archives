"""
    @file: service.py
    @Author:Wang Shihan
    @Date:2023/10/22
    @Description: 服务
"""

from datetime import datetime

# import time
from concurrent.futures import ThreadPoolExecutor
from Mylog import app
from Mylog import db
from sqlalchemy import extract
from Mylog.models import Viewer
from Mylog.util.tool import IPChecker


class Locator:
    _instance = None
    _init = True

    def __init__(self, workers: int = 10) -> None:
        if Locator._init:
            self.excutor = ThreadPoolExecutor(max_workers=workers)
            Locator._init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            Locator._instance = object.__new__(cls)
        return Locator._instance

    def __locator__(
        self, ip: str, ua: str, device: str, referer: str, page: str, token: str
    ):
        """
        记录访问
        :param req:请求
        :param page: 页面
        :return:
        """
        # time.sleep(20)
        with app.app_context():
            try:
                now = datetime.now()
                v = Viewer.query.filter(
                    Viewer.page == page,
                    Viewer.ip == ip,
                    extract('day', Viewer.latest) == now.day,
                    extract('month', Viewer.latest) == now.month,
                    extract('year', Viewer.latest) == now.year,
                ).first()
                if v is None:
                    ip_info = IPChecker(app.config['GEO_DECODE_AK']).check(ip)
                    v = Viewer(
                        ip=ip,
                        country=ip_info.country,
                        province=ip_info.province,
                        city=ip_info.city,
                        lon=ip_info.lon,
                        lat=ip_info.lat,
                        page=page,
                        latest=now,
                        token=token,
                        note='',
                        count=0,
                        device=device,
                        ua=ua,
                        referer=referer,
                    )
                else:
                    v.latest = now
                db.session.add(v)
                db.session.commit()
                app.logger.info(f'记录访问{page}成功')
            except Exception as e:
                app.logger.error(str(e))

    def locator(self, *args, **kwargs):
        self.excutor.submit(self.__locator__, *args, **kwargs)
        # self.__locator__(*args, **kwargs)


if __name__ == '__main__':
    pass
