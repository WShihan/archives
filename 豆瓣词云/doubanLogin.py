# -*- coding: utf-8 -*-
"""
@Date: 2021/5/16 10:48
@Author:Wang Shihan
@File: doubanLogin.py
@Software: PyCharm
"""
import requests
import  pickle as pk
from fake_useragent import UserAgent

class DoubanLogin():
    def __init__(self):
        self.session = requests.session()
        self.loginUrl = 'https://accounts.douban.com/j/mobile/login/basic'
        self.header = {
            'user-agent':UserAgent().ie,
            'referer': 'https://accounts.douban.com/passport/login?source=movie'
        }

    def login(self,username=None, password=None):
        fromData = {
            'name':username,
            'password':password,
            'remember':'false'
        }

        try:
            res = self.session.post(self.loginUrl, headers=self.header, data=fromData)
            res.raise_for_status()
            returnData = res.json()
            if returnData['status'] == "failed":
                return returnData['description']
            else:
                cookie = requests.utils.cookiejar_from_dict(self.session.cookies)
                with open('douban_cookie.pkl','wb') as f:
                    pk.dump(cookie,f)
                return cookie

        except Exception as e:
            print("登录异常:",e)





if __name__ == '__main__':
    douban = DoubanLogin()
    info = douban.login('17869182428', '17869182428')
    print(info)
