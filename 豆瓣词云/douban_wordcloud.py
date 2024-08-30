# -*- coding: utf-8 -*-
"""
@Date: 2021/2/9 21:05
@Author:Wang Shihan
@File: douban_analysis.py
@Software: PyCharm
"""

from wordcloud import WordCloud ,ImageColorGenerator
import jieba.analyse
import os
import numpy as np
from PIL import  Image
import matplotlib.pyplot as plt

cwd = os.getcwd()

comments = open(cwd + '\\comments.txt' , 'r' ,encoding='utf-8').read()
freq = jieba.analyse.extract_tags(sentence=comments , topK=200,withWeight=True)
freq = {i[0]:i[1] for i in freq}


mask = np.array(Image.open('redflower.jpg'))

color = ImageColorGenerator(mask)

wd = WordCloud(
    width=600,
    height=1000,
    font_path='黑体.ttc',  # 指定字体
    mode='RGBA' ,   # 颜色模型
    max_font_size=20,   # 最大字体
    random_state=100,# 随机种子
    mask = mask,    # 掩膜,
    color_func=color,
    scale=11.0,# 计算过程和实际绘图的比例，参数大小和分辨率正相关，浮点型
    background_color='white',  # 背景色
    relative_scaling=0.5,    # 单词出现频率对其字体大小的权重
    ).generate_from_frequencies(freq)


wd.to_array()
plt.imshow(wd, interpolation="bilinear")
plt.axis('off')
plt.show()
wd.to_file('douban.png')