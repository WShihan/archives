# -*- coding: utf-8 -*-
"""
    @file: log.py
    @Author:Wang Shihan
    @Date:2023/9/20
    @Description:日志文件
"""
import os
import time
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler

date_now = time.strftime('%Y-%m-%d', time.localtime())
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'logs')
LOG_DIR_ERROR = os.path.join(LOG_PATH, 'error')
LOG_DIR_INFO = os.path.join(LOG_PATH, 'info')

if not os.path.exists(LOG_DIR_ERROR):
    os.makedirs(os.path.join(LOG_PATH, 'error'))

if not os.path.exists(LOG_DIR_INFO):
    os.makedirs(os.path.join(LOG_PATH, 'info'))

LOG_PATH_ERROR = os.path.join(LOG_DIR_ERROR, f'{date_now}.log')
LOG_PATH_INFO = os.path.join(LOG_DIR_INFO, f'{date_now}.log')

# 启动的日志文件类型
active_loger_dic = dict(
    zip([LOG_PATH_INFO, LOG_PATH_ERROR], [logging.INFO, logging.ERROR])
)

# 日志文件最大 30MB
LOG_FILE_MAX_BYTES = 30 * 1024 * 1024
# 轮转数量是 1 个
LOG_FILE_BACKUP_COUNT = 1


class Logger(object):
    def init_app(self, app):
        # 移除默认的handler
        app.logger.removeHandler(default_handler)
        formatter = logging.Formatter(
            '%(asctime)s [%(thread)d:%(threadName)s] [%(filename)s:%(module)s:%(funcName)s] '
            '[%(levelname)s]: %(message)s'
        )

        for log_path, log_type in active_loger_dic.items():
            # 将日志输出到文件
            # 1 MB = 1024 * 1024 bytes
            # 此处设置日志文件大小为100MB，超过500MB自动开始写入新的日志文件，历史文件归档
            file_handler = RotatingFileHandler(
                filename=log_path,
                mode='a',
                maxBytes=LOG_FILE_MAX_BYTES,
                backupCount=LOG_FILE_BACKUP_COUNT,
                encoding='utf-8',
            )

            file_handler.setFormatter(formatter)
            file_handler.setLevel(log_type)

            stream_handler = StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(log_type)

            for logger in (
                # 这里自己还可以添加更多的日志模块，具体请参阅Flask官方文档
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug'),
            ):
                logger.addHandler(file_handler)
                logger.addHandler(stream_handler)
