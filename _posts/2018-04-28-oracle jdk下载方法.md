---
layout: post
title: "oracle jdk下载方法"
date: 2018-04-28
comments: false
categories: 技巧
---

wget下载oracle jdk需要加上`--no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie"`，否则无法下载.

```bash
wget --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/10.0.1+10/fb4372174a714e6b8c52526dc134031e/jdk-10.0.1_linux-x64_bin.rpm
```
