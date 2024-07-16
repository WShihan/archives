# -*- coding: utf-8 -*-
"""
@Date: 2021/4/15 10:47
@Author:Wang Shihan
@File: QqMusic.py
@Software: PyCharm
"""
import requests
from fake_useragent import UserAgent
import sqlite3
import threading
import csv
from time import localtime
from time import strftime


class Sqlite():
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def exe(self, cmd):
        self.exe(cmd)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()



class QqMusic():
    def __init__(self, page:int):
        self.urls = ["https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk_new_20200303=5381&g_tk=5381&loginUin" \
                   "=0&hostUin=0&format=json&inCharset=utf8&outCharset=GB2312&notice=0&platform=yqq.json&needNewCode=0&" \
                   "cid=205360772&reqtype=2&biztype=1&topid=97784&cmd=8&needmusiccrit=0&pagenum=%s&pagesize=25" % i for i in range(1,page + 1)]
        self.headers = {
            'user-agent':UserAgent().ie,
            'referer':': https://y.qq.com/',
            'origin':'https://y.qq.com'
        }

    def crawler(self, url=None) -> list:
        """
        :param url:
        :return:
        """
        res = requests.get(url, headers=self.headers)
        if res.status_code == 200:
            json_list = res.json()['comment']['commentlist']
            return json_list

    def test(self, json_list):
        comment_dict = {}
        for item in json_list:
            # 获取评论内容，昵称及其日期
            content = item['rootcommentcontent'].strip()
            nick = item['nick'].strip()
            comment_dict[nick] = content
            comment_dict['date'] = strftime("%Y-%m-%d", localtime(item['time']))

        print("--------解析完一页----------")
        print(comment_dict)


    def commenter(self, json_list) -> list:
        """
        :param json_list:
        :return:
        """
        comment_list = []
        for item in json_list:
            content = item['rootcommentcontent'].strip()  # 评论内容
            nick = item['nick'].strip()
            date = strftime("%Y-%m-%d",localtime(item['time']))
            comment_list.append({'nick':nick,'content':content,'date':date})


        return comment_list

    def eternal(self, comment_list, sqlit=False, csv_file=True, mysql=False):
        """
        :param comment_list:
        :param sqlit:
        :param csv_file:
        :param mysql:
        :return:
        """
        if csv_file:

            with open('轨迹.csv','a',encoding='utf-8-sig',newline="") as f:
                handle = csv.writer(f)
                for item in comment_list:
                    #print([item['nick'], item['content'], item['date']])
                    handle.writerow([item['nick'],item['content'],item['date']])



def main(q):
    res = q.commenter(q.crawler(url=i))
    q.eternal(res)
    print("解析完成一页")



if __name__ == '__main__':
    q = QqMusic(635)
    for i in q.urls:
        t = threading.Thread(target=main,args=(q,))
        t.start()

