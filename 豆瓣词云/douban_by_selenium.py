# -*- coding: utf-8 -*-
"""
@Date: 2021/5/20 17:19
@Author:Wang Shihan
@File: douban_by_selenium.py
@Software: PyCharm
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import  sleep



class Douban_by_selenium():
    def __init__(self):
        self.web = webdriver.Chrome()
        self.opt = Options()

    def get(self):
        self.web.get('https://accounts.douban.com/passport/login?source=movie')


if __name__ == '__main__':
    d = Douban_by_selenium()
    d.get()
    sleep(60)

