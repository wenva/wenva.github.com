---
layout: post
title: "python构建WEB服务器"
date: 2015-11-06
comments: false
categories: 
---
本文将利用web.py来快速构建一个WEB服务器，看下面
test.py
<pre>

import web
 
urls=(
    '/','index',
)
app = web.application(urls,globals())

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == '__main__':
        app.run()
</pre>
没错，就上面这么多，当然还得装下web.py

<pre>
sudo easy_install web.py
</pre>

运行上面的py代码
<pre>
python test.py
</pre>

成功后，会打印如下信息
<pre>
http://0.0.0.0:8080/
</pre>

在网页中输入http://127.0.0.1/8080/就可以看到Hello, world!