---
layout: post
title: "利用CGI快速构建HTTP API服务"
date: 2017-05-22
comments: false
categories: 框架
---

为了保证跨平台访问，最好的方式就是通过HTTP API方式，而HTTP API框架很多，有web.py、flask，但缺乏灵活性，只能用某种特定语言编写；而CGI则是语言无关，利用stdin、stdout进行数据传输，那么如何构建.


### 1. 安装Apache2

```
sudo apt-get install apache2
```

### 2. 开启CGI

```
sudo ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load
sudo ln -s /etc/apache2/conf-available/serve-cgi-bin.conf /etc/apache2/conf-enabled/serve-cgi-bin.conf

sudo service apache2 restart
```

### 3. 编写CGI

```
sudo vim /usr/lib/cgi-bin/hello


#!/bin/bash
echo ''   # 需要输出空行，标识HTTP RESPONSE 头结束
echo hello cgi
```

增加可可执行权限
```
sudo chmod +x hello
```

### 4. 访问

```
osmc@osmc:/usr/lib/cgi-bin$ curl http://192.168.0.102/cgi-bin/hello
hello cgi
```

到此HTTP API框架已构建完成，你可以利用任意语言编写CGI脚本


