#-*- coding:utf-8 -*-
"""
@Time: 2020/1/3012:07
@Author:Shihan Wong
@File: 500强企业爬取.py
@Software: PyCharm
"""
import requests , bs4
from bs4 import BeautifulSoup
import csv

# getHTMLtext函数功能：利用requests模块获得HTML代码 ，形式参数url为网页统一资源定位符
def getHTMLtext(url):
    try:
        re = requests.get(url ,timeout = 30)                        # 获取HTML源码
        re.raise_for_status()                                       # 查看状态
        re.encoding = re.apparent_encoding                          # 替换编码
        return re.text                                              # 返回HTML文本
    except Exception as e:                                          # 如果错误，输出e
        print(e)

# saveCompany函数功能：利用BeautifulSoup类解析HTML文本，然后保存解析后的信息
def sveCompany(clist , html):                                       # 形参clist为用户定义用来储存爬取信息的列表，html为之前返回的HTML文本
    soup = BeautifulSoup(html , "html.parser")                      # 解析HTML文本
    for tr in soup.find('tbody').children:                          # 500强信息经查看后发现在'tbody'标签内，遍历其子标签
        if isinstance(tr , bs4.element.Tag):                        # 判断tr是否为标签
            tds = tr('td')                                          # 500强信息'tbody'标签的子标签'tr'标签的子标签'td'内，遍历返回子标签列表后保存在变量tds内
            clist.append([tds[0].string , tds[2].string , tds[5].string])                       # 将爬取的信息保存在设定好的列表内，第一个为排名，二为企业名称，三为国家

# printCompany函数功能：输出保存后的企业信息
def printCompany(clist , num):                                      # 形参clist为之前保存得企业信息，num为用户输入的数字，控制打印的企业数量

    tlt = "{0:^15}\t{1:{3}^60}\t{2:>5}"
    #print("{0:^15}\t{1:{3}^60}\t{2:>5}".format("排名" , "企业名称" , "国家" , chr(12288)))    # 打印输出标题
    for i in range(len(clist)):
        u = clist[i]
        #print(tlt.format(u[0] , u[1] , u[2] , chr(12288)))
        with open('company2019.csv','a' , encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            #writer.writerow([u[0],u[1],u[2]])
            print(u)



def main():                                                          # 定义主函数，调用getHTMLtext(),saveCompany(),printCompany()函数
    sinfo = []
    url = 'http://www.fortunechina.com/fortune500/c/2019-07/22/content_339535.htm'
    html = getHTMLtext(url)
    sveCompany(sinfo , html)
    printCompany(sinfo , 100)

main()    # 调用main函数

