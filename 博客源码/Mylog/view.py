# -*- coding: utf-8 -*-
"""
    @file: view.py
    @Author:Wang Shihan
    @Date:2023/10/22
    @Description:
"""
from typing import List
from functools import wraps
from flask import render_template
from flask import make_response
from flask import request, Request
from flask import send_from_directory
from sqlalchemy import desc, or_, extract
from feedgen.feed import FeedGenerator
from datetime import timezone, timedelta, datetime

from Mylog import app, db, cache
from Mylog.util.tool import (
    SiteMap,
    extract_device,
    extract_ip,
    parse_token,
    show_except,
)
from Mylog.util.service import Locator
from Mylog.models import Blog, User, Cover, BlogType
from Mylog.models import Blog, User, Cover, BlogType
from Mylog.filter import intro2html
from Mylog.store.blog import BlogService
from Mylog.hooks import page_gard


service = BlogService()
domain = app.config['DOMAIN']
SITE_NAME = app.config.get('SITE_NAME', 'Mylog')
SITE_OWNER = app.config.get('SITE_OWNER', 'Mylog')
SITE_EMAIL = app.config.get('SITE_EMAIL', 'Mylog')
SITE_DESCRIPTION = app.config.get('SITE_DESCRIPTION', 'Mylog 一个网站')


class Router:
    """路由对象"""

    def __init__(self, label, link: str = None):
        self.label = label
        self.link = link


def start_locator(req: Request, page: str):
    Locator(10).locator(
        extract_ip(req),
        req.user_agent.string,
        extract_device(req.user_agent.string),
        req.referrer,
        page,
        parse_token(request.headers.get('Cookie')),
    )


def calc_blog_category(blogs: List[Blog]) -> dict:
    stat_dict = dict()
    for blog in blogs:
        if stat_dict.get(blog.category):
            stat_dict[blog.category] += 1
        else:
            stat_dict[blog.category] = 1
    return stat_dict


@app.after_request
def after_request(response):
    # 加入限制镜像的条件
    # 防止页面被嵌入到 iframe 中
    response.headers['X-Frame-Options'] = 'DENY'
    # 防止 MIME 类型嗅探
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(str(e))
    return (
        render_template(
            'status.html',
            msg="您访问的页面不存在！The page you request is not found!",
            title="页面不存在",
            nav=Router('错误页面'),
            code=404,
        ),
        404,
    )


@app.errorhandler(403)
def page_forbidden(e):
    app.logger.error(str(e))
    return (
        render_template(
            'status.html',
            msg="权限错误",
            title="权限错误",
            code=403,
            nav=Router('错误页面'),
        ),
        403,
    )


@app.errorhandler(401)
def page_unauthorization(e):
    app.logger.error(str(e))
    return (
        render_template(
            'status.html',
            msg="权限错误",
            title="权限错误",
            code=401,
            nav=Router('错误页面'),
        ),
        401,
    )


@app.errorhandler(500)
def page_internal_error(e):
    app.logger.error(str(e))
    return (
        render_template(
            'status.html',
            msg="网站出错了",
            title="网站出错了",
            code=500,
            nav=Router('错误页面'),
        ),
        500,
    )


# 注册访问
def register_viewer(page):
    """
    放网注册装饰器
    :param page:
    :return:
    """

    def decrator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            start_locator(request, page)
            return func(*args, **kwargs)

        return decorated_function

    return decrator


def save_or_update(obj):
    db.session.add(obj)
    db.session.commit()


# 网站地图
@app.route('/sitemap.xml')
def gen_sitemap():
    site = SiteMap()
    root = f"https://{domain}"
    site.add_url(
        {'loc': root, 'priority': 1, 'changefreq': 'weekly', 'lastmod': '2024-02-12'}
    )
    site.add_url(
        {
            'loc': root + '/feed.xml',
            'priority': 1,
            'changefreq': 'weekly',
            'lastmod': '2024-02-12',
        }
    )
    site.add_url(
        {
            'loc': root + '/whisper',
            'priority': 0.8,
            'changefreq': 'weekly',
            'lastmod': '2024-02-12',
        }
    )
    site.add_url(
        {
            'loc': root + '/moment',
            'priority': 0.8,
            'changefreq': 'weekly',
            'lastmod': '2024-02-12',
        }
    )
    site.add_url(
        {
            'loc': root + '/blogs',
            'priority': 1,
            'changefreq': 'weekly',
            'lastmod': '2024-02-12',
        }
    )
    site.add_url(
        {
            'loc': root + '/about',
            'priority': 1,
            'changefreq': 'weekly',
            'lastmod': '2024-02-12',
        }
    )

    for b in service.get_visible_blog(BlogType.BLOG):
        site.add_url(
            {
                'loc': root + '/blog/%s' % (b.id),
                'lastmod': b.time.strftime('%Y-%m-%d'),
                'priority': 0.8,
                'changefreq': 'monthly',
            }
        )

    xml = site.to_string()
    resp = make_response(xml)
    resp.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return resp


@cache.cached(key_prefix='feed')
def generate_feed():
    tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00
    # 创建一个Feed对象
    fg = FeedGenerator()
    fg.id(f'https://{domain}')
    fg.author({'name': SITE_OWNER, 'email': SITE_EMAIL})
    fg.title(SITE_NAME)
    fg.language('zh-CN')
    fg.description(SITE_DESCRIPTION)
    fg.link(href=f"https://{domain}")
    fg.logo(f"https://{domain}/static/Favicon.ico")
    blogs = service.get_visible_blog(BlogType.BLOG)
    blogs.reverse()
    for blog in blogs:
        fe = fg.add_entry()
        link = f"https://{domain}/blog" + '/' + blog.id
        description = (
            f'<p>{intro2html(blog.intro.rstrip("。") + "……")}</p>'
            if blog.intro
            else blog.title
        )
        fe.title(f'{blog.title}\t#{blog.category}#')
        fe.category({'term': blog.category, 'label': blog.category})
        fe.link(href=link)
        fe.summary(description, type='html')
        fe.guid(link, permalink=True)
        fe.author(name=SITE_OWNER, email=SITE_EMAIL)
        fe.pubDate(blog.time.replace(tzinfo=tz_utc_8))
        if blog.update:
            fe.updated(blog.update.replace(tzinfo=tz_utc_8))
    response = make_response(fg.atom_str(pretty=True))
    response.headers.set('Content-Type', 'application/xml; charset=utf-8')
    return response


@app.route('/<regex("^rss(.xml)?"):url>')
@register_viewer('rss.xml')
def rss_xml(url):
    return generate_feed()


@app.route('/<regex("^feed(.xml)?"):url>')
@register_viewer('feed')
def make_feed(url):
    return generate_feed()


@app.route('/<path:filename>')
def varify_search_engine(filename):
    try:
        path = "./templates"
        return send_from_directory(path, filename)
    except Exception as e:
        return str(e)


# 上传文件
# 获取图片
@app.route('/file/<path:filename>')
def uploaded_files(filename):
    path = 'static/img/blog'
    return send_from_directory(path, filename)


# 文档
@app.route('/doc/<path:name>')
def doc_reader(name):
    return render_template('docs/' + name)


@app.route('/')
@register_viewer('index')
@page_gard
@cache.cached(key_prefix='index')
def index():
    try:
        user = User.query.filter().first()
        return render_template(
            'index.html',
            content=user.index,
            title=SITE_NAME,
            desc=SITE_DESCRIPTION,
            styles=["index.css"],
        )
    except Exception as e:
        return show_except(msg=str(e), error=e)


@app.route('/admin')
@page_gard
def index_admin():
    try:
        return render_template(
            'admin.html',
        )
    except Exception as e:
        return show_except(msg=str(e), error=e)


@app.route('/blogs')
@register_viewer('blogs')
@page_gard
@cache.cached(key_prefix='blogs')
def blogs_all():
    try:
        search = request.args.get('search', '')
        args = []
        query = Blog.query.filter(
            Blog.type == BlogType.BLOG,
            Blog.visible == True,
            Blog.publish == True,
        )
        subs = calc_blog_category(query.all())
        if search != '':
            blogs = (
                query.filter(
                    or_(
                        Blog.title.like(f'%{search}%'),
                        Blog.category.like(f'%{search}%'),
                    )
                )
                .order_by(Blog.time.desc())
                .all()
            )
            args.append(f'&search={search}')
        else:
            common_blogs = (
                query.filter(
                    Blog.pin == False,
                )
                .order_by(Blog.time.desc())
                .all()
            )
            pin_blogs = query.filter(Blog.pin == True).order_by(Blog.time.desc()).all()
            blogs = pin_blogs + common_blogs

        return render_template(
            'blogs.html',
            title="博文·全部",
            blogs=blogs,
            search=search,
            nav=Router('博文'),
            desc=f"{SITE_DESCRIPTION} 博文列表",
            styles=['blogs.css'],
            subs=subs,
        )
    except Exception as e:
        return show_except(msg='出错', error=e)


@app.route('/blogs/<string:topic>')
@register_viewer('blogs/topic')
@page_gard
def blogs_category(topic: str):
    try:
        search = request.args.get('search', '')
        blogs = Blog.query.filter(
            Blog.type == BlogType.BLOG, Blog.visible == True, Blog.category == topic
        ).all()
        return render_template(
            'blogs.html',
            title=f"博文·{topic}",
            blogs=blogs,
            search=search,
            nav=[Router('博文', '/blogs'), Router(topic)],
            desc=f"{SITE_DESCRIPTION} {topic}博文列表",
            styles=['blogs.css'],
        )

    except Exception as e:
        return show_except(msg=f'出错{str(e)}', error=e)


@app.route('/blog/<string:id>')
@page_gard
def single_blog(id: str):
    try:
        blog = Blog.query.filter(Blog.id == id).first()
        start_locator(request, blog.title)
        save_or_update(blog)
        return render_template(
            'blog.html',
            title=blog.title,
            blog=blog,
            nav=[Router('博文', '/blogs'), Router(blog.title)],
            desc=f"#{blog.category} {blog.intro}",
            styles=["blog.css"],
        )
    except Exception as e:
        return show_except(msg=f"您请求的资源不存在", error=e)


@app.route('/all-about-gis')
@page_gard
def all_about_gis():
    publications = service.get_visible_blog(BlogType.PUBLICATION)
    return render_template(
        'all-about-gis.html',
        title="All about GIS",
        publications=publications,
        nav=Router('All-about-GIS'),
        desc="All about GIS, evrything related to gis only",
        styles=['all-about-gis.css'],
    )


@app.route('/all-about-gis/<id>')
@page_gard
def all_about_gis_single(id):
    try:
        publication = Blog.query.filter(Blog.id == id).first()
        publication.visited += 1
        start_locator(request, publication.title)
        return render_template(
            'blog.html',
            title='All about GIS-' + publication.id,
            blog=publication,
            nav=[Router('All-about-GIS', '/all-about-gis'), Router(publication.id)],
            styles=['blog.css'],
        )
    except Exception as e:
        return show_except(msg="您请求的资源不存在", error=e)


@app.route('/all-about-gis/feed.xml')
@register_viewer('all-about-gis-rss.xml')
def all_about_gis_feed():
    tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00
    fg = FeedGenerator()
    fg.id('https://www.wsh233.cn/all-about-gis/')
    fg.author({'name': '王世涵', 'email': '3443327820@qq.com'})
    fg.title('All about GIS')
    fg.language('zh-CN')
    fg.description('all about gis，只关于GIS，分享相关文章，工具，数据等。')
    fg.link(href=f'https://{domain}/all-about-gis')
    fg.logo(f"https://{domain}/static/Favicon.ico")

    for pub in service.get_visible_blog(BlogType.PUBLICATION):
        fe = fg.add_entry()
        link = f"https://{domain}/all-about-gis" + '/' + pub.id
        fe.guid(link, permalink=True)
        description = intro2html(pub.body)
        fe.title(f'All about GIS·{pub.id}\t#信息合集#')
        fe.category({'term': '信息合集', 'label': '信息合集'})
        fe.link(href=link)
        fe.summary(summary=description, type='html')
        fe.author(name='all-about-gis', email='3443327820@qq.com')
        fe.pubDate(pub.time.replace(tzinfo=tz_utc_8))
    response = make_response(fg.atom_str(pretty=True))
    response.headers.set('Content-Type', 'application/xml; charset=utf-8')
    return response


@app.route('/whisper')
@register_viewer('whisper')
@page_gard
@cache.cached(key_prefix='whisper')
def whisper():
    diaries = Blog.query.filter(Blog.type == 1).order_by(Blog.time.desc()).all()
    subs = {}
    for item in diaries:
        if subs.get(item.time.year):
            subs[item.time.year] += 1
        else:
            subs[item.time.year] = 1
    return render_template(
        'whisper.html',
        title='日志',
        diary=diaries,
        subs=subs,
        nav=Router('日志'),
        desc=f"{SITE_DESCRIPTION}，日志页面。",
        styles=['whisper.css'],
    )


@app.route('/whisper/<year>')
@register_viewer('whisper/year')
@page_gard
def whisper_by_year(year):
    diaries = (
        Blog.query.filter(Blog.type == 1, extract('year', Blog.time) == year)
        .order_by(Blog.time.desc())
        .all()
    )
    return render_template(
        'whisper.html',
        title='日志',
        diary=diaries,
        nav=[Router('日志', '/whisper'), Router(f'{year}年')],
        desc=f"{SITE_DESCRIPTION}，日志页面。",
        styles=['whisper.css'],
    )


@app.route('/about')
@register_viewer('about')
@page_gard
@cache.cached(key_prefix='about')
def about():
    lu = User.query.filter().first()
    about_text = lu.about if lu is not None else ''
    return render_template(
        'about.html', about_text=about_text, nav=Router('关于'), styles=['index.css']
    )


@app.route('/moment')
@register_viewer('moment')
@page_gard
@cache.cached(key_prefix='moment')
def moment():
    ones = Cover.query.order_by(desc(Cover.time))[0:]
    time_range = ones[0].time.year if len(ones) > 1 else datetime.now().year
    subs = {}
    for one in ones:
        if subs.get(one.time.year):
            subs[one.time.year] += 1
        else:
            subs[one.time.year] = 1

    return render_template(
        'moment.html',
        ones=ones,
        subs=subs,
        title=f'时刻 | 2018-{time_range}',
        nav=Router('时刻'),
        desc=f"{SITE_DESCRIPTION}，时刻。",
        styles=['moment.css'],
    )


@app.route('/whisper/create')
def moment_create():
    ones = Cover.query.order_by(desc(Cover.time))[0:]
    return render_template(
        'whisper-create.html',
        ones=ones,
        title=f'创建日志',
        nav=Router('创建日志'),
        desc=f"{SITE_DESCRIPTION}，moment页面。",
        styles=['index.css'],
    )


@app.route('/moment/<int:year>')
@register_viewer('moment/year')
@page_gard
def moment_by_year(year: int):
    ones = []
    for one in Cover.query.order_by(desc(Cover.time))[0:]:
        if one.time.year == year:
            ones.append(one)

    return render_template(
        'moment.html',
        title=f'时刻 | {str(year)}',
        ones=ones,
        pre=year - 1,
        next=year + 1,
        nav=[Router('时刻', '/moment'), Router(f'{year}年')],
        desc=f"{SITE_DESCRIPTION}，时刻页面，{year}年。",
        styles=['moment.css'],
    )


@app.route('/robots.txt')
def send_robot():
    return send_from_directory('static', f'file/robots.txt')
