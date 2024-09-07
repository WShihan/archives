Mylog
====
一个简单的Python博客，使用flask及其相关插件完成，👀 在线 [demo](https://www.wsh233.cn)。

特点：

* 简洁，去除与阅读无关的要素。
* 自带博客后台且前后端分开。
* 支持渲染mermaid图表。
* 支持渲染MacOS窗口风格的代码块。
* 支持缓存。
* 支持访问统计。
* 支持RSS

使用
====

1.环境配置

下载整个项目代码后，创建虚拟环境

```bash
poetry shell
```



安装依赖

```bash
poetry install
```



2.修改Mylog目录下的`settings.py`文件的配置项

3.初始化数据库

```bash
flask db init
flask migrate
flask upgrade
```

创建初始用户

```bash
flask init
```



4.启动

cmd进入项目位置，允许`run.py`文件或运用如下命令

```bash
flask run
```
