# -*- coding: utf-8 -*-
# @author wangshihan
# @date 2024-08-15
# @description csv文件编码转换器
import argparse
import os
import csv
import logging

VERSION = '0.0.1'
logging.basicConfig(level=logging.INFO)


def init_args() -> argparse.Namespace:
    """初始化参数
    Raises:
        ValueError: 错误

    Returns:
        argparse.Namespace: 参数
    """
    parser = argparse.ArgumentParser(
        prog='csvc',
        description=f'''
        CSV Convertor: convert CSV file's encoding
        作者：WangShihan\n
        版本：{VERSION}
        ''',
        epilog='wangshihan'
    )
    parser.add_argument('--f', required=True, type=str,help="当处理单文件时为csv文件，当批处理时为目录。")
    parser.add_argument('--d', required=False, type=str, default='utf-8', help='解码格式，默认为utf-8。')
    parser.add_argument('--e', required=False, type=str, default='gbk', help='编码格式，默认为gbk。')

    args = parser.parse_args()
    logging.info('检验参数及配置')
    if os.path.exists(args.f) is False:
        raise ValueError('无法获取vidycsv文件，请检查路径！')
    return args


def tip(msg, sign='-'):
    fmt = '{0:%s^100}' % sign
    return fmt.format(msg)

def covertor(file: str, decoding: str, encoding: str):
    """转换编码格式
    Args:
        file (str): 文件路径
        decoding (str): 原始编码
        encoding (str): 目标编码
    """
    faileds = []
    reader = csv.DictReader(open(file, 'r', encoding=decoding))
    writer = csv.DictWriter(open(file.split('.')[0] + f'_{encoding}.csv', 'w', encoding=encoding), fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        try:
            writer.writerow(row)
        except Exception as e:
            faileds.append(row)
            logging.error('转换失败，记录：{0}'.format(e))

    logging.info(f'转换失败记录：{len(faileds)}')
    logging.info(tip('转换完毕', '='))


def batch_convertor(path: str, decoding: str, encoding: str):
    tasks = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv') and not file.endswith(f'_{encoding}.csv'):
                tasks.append(os.path.join(root, file))

    while len(tasks) > 0:
        try:
            task = tasks.pop(0)
            logging.info(tip(f'开始转换{task}'))
            covertor(task, decoding, encoding)
        except Exception as e:
            logging.error(f'转换失败{task}：{e}')


def main():
    try:
        args = init_args()
        if os.path.isdir(args.f):
            batch_convertor(args.f, args.d, args.e)
        else:
            logging.info(tip(f'开始转换{args.f}'))
            covertor(args.f, args.d, args.e)
    except Exception as e:
        logging.error(f'错误：{e}')


if __name__ == "__main__":
    main()
