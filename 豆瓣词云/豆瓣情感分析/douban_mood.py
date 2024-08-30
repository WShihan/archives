# -*- coding: utf-8 -*-
"""
@Date: 2021/2/11 16:37
@Author:Wang Shihan
@File: douban_mood.py
@Software: PyCharm
"""

from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
import csv



file = open('comment.csv' , 'r' , encoding='utf-8-sig')
comm = [c[1] for c in csv.reader(file)]
sentiments_list = []

# 计算每一行情感分数
for c in comm:
    score = SnowNLP(c).sentiments
    sentiments_list.append(score)
#print(sentiments_list)
change = np.gradient(np.array(sentiments_list))
plt.figure(figsize=(50,50))
plt.hist(sentiments_list,bins=100,density=True,stacked=True,histtype="stepfilled",facecolor='b',alpha=0.75)
plt.grid(True)
plt.show()

"""
# 折线图
plt.plot(change,color="red")

fontdict={"fontproperties":"SimHei","fontsize":15}
plt.xlabel("序号",fontdict=fontdict)
plt.ylabel("梯度分值",fontdict=fontdict)
plt.title("豆瓣影评情感得分梯度折线图",fontproperties="SimHei",fontsize=20)
#plt.savefig("梯度折线图.png")
plt.show()"""

"""
#直方图
print(len(sentiments_list),sentiments_list)
plt.hist(sentiments_list , bins=np.arange(0,1,0.01),facecolor='g')
plt.xlabel('Sentiments Probability')
plt.ylabel('Quality')
plt.title("Analysis Of  Douban Sentiments")
plt.show()"""