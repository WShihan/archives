# -*- coding: utf-8 -*-
"""
    @Date:  2022-05-22
    @Author:Wang Shihan
"""
import click
from Mylog import db
from Mylog import app
from Mylog.models import User, Blog

index_text = '''
[博文](/blogs)｜[日志](/whisper)｜[时刻](/moment)｜[关于](/about)

Hello

大家好，我是🙍，这是我的个人博客，欢迎你们👏。
'''

first_blog_content = '''
[TOC]

# 这是第一个一级标题 

你好啊

# 这是第二个一级标题

你好啊

## 这是第一个二级标题

你好啊

'''


def gen_admin():
    user = User(
        name='admin',
        password='test123',
        about='这是关于页面文字',
        index=index_text,
    )
    db.session.add(user)
    db.session.commit()
    click.echo("创建初始用户成功！")


def gen_blog():
    blog = Blog(
        id=0,
        type=0,
        title='第一篇博客',
        intro='第一篇博文介绍',
        body=first_blog_content,
        category='杂',
        visible=True,
    )
    db.session.add(blog)
    db.session.commit()
    click.echo("创建第一篇博文成功！")


@app.cli.command()
@click.option('--drop', is_flag=False, help="创建前是否清除数据库！")
def init(drop):
    if drop:
        click.confirm("该操作将会清除数据库，是否执行？", abort=True)
        db.drop_all()
        click.echo("删除表……")
        db.create_all()
    click.echo("重新初始化数据库成功！")
    gen_admin()
    gen_blog()
    click.echo("初始化数据库完成！")
