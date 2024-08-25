# -*- coding: utf-8 -*-
"""
    @file: bge.py
    @Author: WangShihan
    @Date: 2024/08/25
    @Description: mp42mp3
"""
import unicodedata
from moviepy.editor import VideoFileClip
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import logging
import argparse
import time


logging.basicConfig(level=logging.INFO)
VERSION = '0.0.1'

# 设置工作目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def extractor(video_path, start: int =0, end: int = 0):
    try:
        logging.info("{0:-^100}".format(f'开始提取：{video_path}'))
        file_name = os.path.splitext(os.path.basename(video_path))[0]
        file_path = os.path.dirname(video_path)
        video = VideoFileClip(video_path)

        # 设置要提取的音频的起始和结束时间（单位为秒）
        # 跳过前 10 秒
        start_time = start  
        # 跳过最后 5 秒
        end_time = video.duration - end

        # 提取音频并保存为 MP3 格式
        audio = video.audio.subclip(start_time, end_time)
        audio.write_audiofile(f"{file_path}/{file_name}.mp3", codec='mp3')
        logging.info("{0:=^100}".format(f'提取完成：{file_path}/{file_name}.mp3'))
    except Exception as e:
        logging.error(f'提取失败：{e}')


def main():
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.prog = 'mp42mp3'
    parser.description = f'''
                    将mp4音频提取为mp3\n
                    作者：WangShihan\n
                    版本：{VERSION}
                '''
    parser.add_argument('-v', required=True, type=str, help='单个mp4文件路径或多个mp4文件所在路径')
    parser.add_argument('-s', type=int, default=0, help='跳过前多少秒（单位为秒）')
    parser.add_argument('-e', type=int, default=0, help='距离结尾多少秒结束（单位为秒）')
    args = parser.parse_args()

    file_path = os.path.abspath(args.v)
    start = args.s
    end = args.e

    if os.path.exists(file_path) is False:
        raise ValueError('无法获取vidycsv文件，请检查路径！')

    if os.path.isdir(file_path):
        logging.info('{:-^100}'.format('指定目录，开始查找mp4文件'))
        videos = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith('.mp4'):
                    logging.info(f'发现mp4文件：{os.path.join(root, file)}')
                    videos.append(os.path.join(root, file))
        for f in videos:
            print(f)

        for i in range(0, len(videos), 10):
            videos_sub = videos[i:i+10]
            with ThreadPoolExecutor(max_workers=10) as executor:
                tasks = [executor.submit(extractor, j, start, end) for j in videos_sub]
                as_completed(tasks)
    else:
        extractor(file_path, start, end)

    logging.info(f'耗时：{time.time() - start_time}秒')

if __name__ == '__main__':
    main()

