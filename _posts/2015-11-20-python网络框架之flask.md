---
layout: post
title: "python网络框架之flask"
date: 2015-11-20
comments: false
categories: 后端
---

常听起有些网站后台是用python来构建的（如豆瓣君），于是teyi去了解下，python的web框架还真不少（python社区果然强大），有django、Tornado、Bottle、flask、web.py等等，在前面『[python构建WEB服务器](python构建WEB服务器.html)』介绍过用web.py来构建网站，当时看起来非常简单，今天我们来介绍另一个框架flask.

Flask是一个使用 Python 编写的轻量级 Web 应用框架。其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2. 可以通过pip安装flask
<pre>
pip install flask
</pre>

下面来个栗子.
<pre>
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():    
    return "Hello World!"
 
if __name__ == "__main__":
    app.run()
</pre>

运行
<pre>
python hello.py
</pre>

浏览器输入http://localhost:5000/即可
