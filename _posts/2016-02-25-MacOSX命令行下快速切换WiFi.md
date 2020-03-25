---
layout: post
title: "MacOSX命令行下快速切换WiFi"
date: 2016-02-25
comments: false
categories: SHELL
---

办公室内有多个WiFi热点，由于工作内容的不同，需要不停地在多个WiFi下切换，而且有些WiFi还需要手动分配IP，如果是使用手动选择WiFi，再配置就非常不方便，因此，需要实现命令行下快速切换WiFi，首先列出一些tips

### 1. Tips

* 查看IP信息
<pre>
ifconfig
</pre>

* 查看DNS
<pre>
networksetup -getdnsservers Wi-Fi
</pre>

* 设置DNS
<pre>
networksetup -setdnsservers Wi-Fi xxx.xxx.xxx.xxx
</pre>

* 查看默认网关
<pre>
netstat -nr|grep default
</pre>

* 删除默认网关
<pre>
sudo route delete default
</pre>
* 添加默认网关
<pre>
sudo route add default xxx.xxx.xxx.xxx
</pre>

* 查看WiFi列表
<pre>
ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport
airport -s
</pre>

* 获取当前WiFi信息
<pre>
airport -I
</pre>

* 手动配置IP
<pre>
networksetup -setmanual networkservice  ip subnet router
或
networksetup -setmanualwithdhcprouter networkservice ip 
</pre>

* 动态分配IP
<pre>
networksetup -setdhcp networkservice
</pre>

* 查看当前网络配置
<pre>
networksetup -getinfo Wi-Fi
</pre>

### 2. 脚本化
配置dd-wrt-xhw为手动分配IP为192.168.8.161
<pre>
networksetup -setmanual Wi-Fi 192.168.8.161 255.255.255.0 192.168.8.1;networksetup -setairportnetwork en0 dd-wrt-xhw password
</pre>
配置22#3F-szjjyfb-AP1_5G为自动获取IP
<pre>
networksetup -setdhcp Wi-Fi;networksetup -setairportnetwork en0 22#3F-szjjyfb-AP1_5G password
</pre>
