# -*- coding: utf-8 -*-
"""
    @file: filter.py
    @Author:Wang Shihan
    @Date:2023/6/9
    @Description:过滤器
"""
import re
import os
from datetime import datetime
import markdown
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension
from Mylog import app


@app.template_filter()
def year_month_filter(dt: datetime) -> str:
    """
    解析日期格式为类似： Feb 2020
    :param dt: datetime.datetime
    :return: str
    """
    return dt.strftime('%b %Y')


# markdown 解析规则，搭配插件使用
RULE = [
    {
        'type': 'post',
        'pat': r'<video(.+?)></video>',
        'value': r'<video controls style="width:100%;"\1></video>',
        'name': 'video 解析',
    },
    {
        'type': 'post',
        'pat': r'<img(.+?)src="(.+?)"(.+?)>',
        'value': r'<a class="lazy-img-wrapper" href="\2" target="_blank"><img class="img lazy-img" data-src="\2" \1 \3 ></a>',
        'name': '图片 解析',
    },
    {
        'type': 'post',
        'pat': r'<pre class="codehilite">(.+?)</pre>',
        "value": r'''    
                <div class="code-win">
                    <div class="code-titlebar">
                        <div class="code-buttons">
                            <div class="code-button close"></div>
                            <div class="code-button minimize"></div>
                            <div class="code-button zoom"></div>
                        </div>
                        <div class="code-copy" data-codeid="%s">复制</div>
                    </div>
                    <div class="code-content"><pre style="line-height:0.2em;" class="codehilite">\1</pre></div>
                </div>''',
        'name': '代码块解析',
    },
    {
        'type': 'pre',
        'pat': r"```mermaid(.+?)```",
        'value': r'<div class="mermaid" style="margin:0px auto;">\1</div>',
        'name': 'mermaid解析',
    },
    {
        'type': 'pre',
        'pat': r'==(.+?)==',
        'value': r'<mark>\1</mark>',
        'name': '高亮解析',
    },
]


class MylogExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(MylogPreprocessor(), 'mermaid_preprocessor', 1000)
        md.postprocessors.register(MylogPostprocessor(), 'custom_preprocessor', 25)


class MylogPreprocessor(Preprocessor):
    def run(self, lines):
        text = '\n'.join(lines)
        rules = [item for item in RULE if item['type'] == 'pre']
        pro_text = text
        post_text = ""
        for r in rules:
            post_text = re.sub(r['pat'], r['value'], pro_text, flags=re.S)
            pro_text = post_text

        return post_text.splitlines()


class MylogPostprocessor(Postprocessor):
    def run(self, text):
        rules = [item for item in RULE if item['type'] == 'post']
        pro_text = text
        post_text = ""
        for r in rules:
            post_text = re.sub(r['pat'], r['value'], pro_text, flags=re.S)
            pro_text = post_text

        return post_text


@app.template_filter()
def md2html(text):
    """
    解析====高亮
    :param text: str
    :return: str
    """

    def add_sections(html):
        lines = html.split('\n')
        new_lines = []
        in_section = False
        for line in lines:
            if line.startswith('<div class="toc">'):
                line = (
                    '<div class="toc-switch" id="toc-switch"><span>目录</span></div>\n'
                    + line
                )

            is_head = re.search(r'^<h\d', line, flags=re.S)
            if is_head is not None:
                id_group = re.search(r'id="(.+?)"', line, flags=re.S)
                if id_group is not None:
                    id = id_group.group(1)
                else:
                    continue
                if in_section:
                    new_lines.append('</section>')
                new_lines.append(f'<section id="{id}">')
                in_section = True
            new_lines.append(line)

        if in_section:
            new_lines.append('</section>')

        return '\n'.join(new_lines)

    html = markdown.markdown(
        text,
        extensions=[
            MylogExtension(),
            'markdown_checklist.extension',
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
        ],
    )
    # print(md)
    return add_sections(html)


@app.template_filter()
def intro2html(text):
    """
    解析====高亮
    :param text: str
    :return: str
    """
    return markdown.markdown(
        text,
        extensions=[
            'markdown_checklist.extension',
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.codehilite',
        ],
    )
    # print(md)


@app.template_filter()
def inner_css(file_name: str) -> str:
    """
    @params file_name: css文件名
    """
    base_dir = app.config.get('BASE_DIR')
    css_path = base_dir + r'/static/css/%s' % file_name
    if not base_dir or not os.path.exists(css_path):
        return ""
    with open(css_path) as f:
        css = f.read()
        return css


@app.template_filter()
def concate(val, *args):
    """
    拼接多个参数为字符串
    :param val:
    :param args:
    :return: str
    """
    res = map(lambda x: str(x), args)
    return str(val).join(res)


@app.template_filter()
def datetime_day(dt: datetime) -> str:
    return str(dt.day)


if __name__ == '__main__':
    text = """
# Section 1
Content of section 1.

## Subsection 1.1
Content of subsection 1.1.

# Section 2
‘’‘python 
def func():
    return 10
'''
Content of section 2.
    """
    md = md2html(text)
    print(md)
