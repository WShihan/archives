# -*- coding: utf-8 -*-
"""
@Date: 2021/4/16 17:04
@Author:Wang Shihan
@File: Qq_comment_sentiment.py
@Software: PyCharm
"""

import matplotlib.pyplot as plt
import pandas as pd
import snownlp

df = pd.read_csv('轨迹.csv', names=['昵称','评论', '日期'])
sentiment_list = []
comment = df['评论']

for c in comment:
    sentiment_list.append(snownlp.SnowNLP(c).sentiments)


