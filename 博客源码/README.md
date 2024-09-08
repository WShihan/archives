## Mylog

一个简单的Python博客，使用flask及其相关插件完成，👀 在线 [demo](https://www.wsh233.cn)。

特点：

* 简洁，去除与阅读无关的要素。
* 自带博客后台且前后端分开。
* 数据库支持使用Sqlite或者PostgreSQL
* 支持渲染Mermaid图表。
* 支持渲染MacOS窗口风格的代码块。
* 支持缓存。
* 支持访问统计。
* 支持RSS
* 支持黑暗模式

## 效果


![image-20240908162239214](https://md-1301600412.cos.ap-nanjing.myqcloud.com/pic/typora/image-20240908162239214.png)

<center style="color: gray">博客首页</center>



![image-20240908162308781](https://md-1301600412.cos.ap-nanjing.myqcloud.com/pic/typora/image-20240908162308781.png)

<center style="color: gray">后端管理页面</center>

## 使用


要求：

* Python >= 3.8



1.环境配置

下载整个项目代码后，创建虚拟环境

```bash
poetry shell
```

安装依赖，可以使用pip安装，

```bash
pip install -r requirements.txt
```

但是这样会污染全局解释器，推荐使用虚拟环境，这里使用`Poetry`，首先先安装它

```bash
pip insall poetry
```

接着使用`Poetry`创建虚拟环境

```bash
poetry shell
```

最后安装依赖

```bash
poetry install
```



2.修改配置

Mylog目录下的`settings.py`文件，包含博客项目所有的的配置项，请先浏览一遍。


3.初始化数据库和初始用户

```bash
flask db init
flask db migrate
flask db upgrade
```

接着初始化默认用户

```bash
flask init
```

默认用户:

* 用户名：admin
* 密码：test123



4.启动

cmd进入项目位置，允许`run.py`文件或运用如下命令

```bash
flask run
```

