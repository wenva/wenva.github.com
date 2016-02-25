---
layout: post
title: "MacOSX平台命令行下网络配置若干TIP"
date: 2016-02-25
comments: false
categories: MacOSX
---

办公室内有多个WiFi热点，由于工作内容的不同，需要不停地在多个WiFi下切换，而且有些WiFi还需要手动分配IP，如果是使用手动选择WiFi，再配置就非常不方便，因此，此处列出脚本化操作关键点

* 查看ip信息
<pre>
ifconfig
</pre>

* 查看路由
<pre>
netstat -nr|grep default
</pre>

* 查看WiFi列表
<pre>

</pre>