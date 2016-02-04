---
layout: post
title: "命令行下获取TP-LINK路由器DHCP客户端列表"
date: 2016-02-04
comments: false
categories: 网络
---

需要实现一个需求：当我回到家时，音乐自动播放起来；关于这个需求有很多方式，比如声音识别、摄像透识别（仿生），当然也可以通过蓝牙、WIFI，声音与摄像识别的难度相对较大，后期再研究，因此就剩下蓝牙和WIFI，蓝牙的话，目前确实蓝牙适配器，因此也暂时不考虑，于是就剩下WIFI了. 总体思路，就是实时监控路由器中是否有我的手机在线，如果在线，则认为我在家. 那么问题就来了，如何知道我手机是否连到路由器. 这里有两个方法，方法一：为手机设置静态ip，不断ping这个ip；方法二：动态获取手机ip，不断ping这个ip.本文主要讲述如何动态获取手机ip.

### 尝试1
希望利用arp命令获取手机的ip，通过`arp -a`会得到如下结果：
<pre>
bogon (192.168.12.1) at d0:c7:c0:8a:1a:7c on en0 ifscope [ethernet]
bogon (192.168.12.51) at d4:be:d9:d9:36:2d on en0 ifscope [ethernet]
bogon (192.168.12.100) at d8:bb:2c:d3:ee:aa on en0 ifscope [ethernet]
bogon (192.168.12.101) at a8:20:66:4a:cb:b6 on en0 ifscope [ethernet]
bogon (192.168.12.103) at a8:66:7f:ea:36:16 on en0 ifscope [ethernet]
bogon (192.168.12.104) at (incomplete) on en0 ifscope [ethernet]
bogon (192.168.12.107) at 78:e4:0:2:e6:93 on en0 ifscope [ethernet]
bogon (192.168.12.109) at 70:e7:2c:cd:52:87 on en0 ifscope [ethernet]
bogon (192.168.12.110) at ac:cf:85:7f:f9:c6 on en0 ifscope [ethernet]
bogon (192.168.12.116) at c:41:3e:e6:7d:e2 on en0 ifscope [ethernet]
bogon (192.168.12.118) at c:1d:af:c3:11:e4 on en0 ifscope [ethernet]
bogon (192.168.12.120) at (incomplete) on en0 ifscope [ethernet]
bogon (192.168.12.122) at (incomplete) on en0 ifscope [ethernet]
bogon (192.168.12.125) at dc:9b:9c:d6:59:ee on en0 ifscope [ethernet]
? (192.168.12.129) at 18:20:32:ad:e6:5c on en0 ifscope [ethernet]
? (192.168.12.255) at (incomplete) on en0 ifscope [ethernet]
</pre>
PS：通过比对mac判断哪个是手机，但是发现个问题，`arp -a`只能查看局域网内通信过的ip信息，对于未通信的终端是没有相应信息的，而且还发现mac有时是无法获取到，如上显示incomplete

### 尝试2
通过模仿web方式查看路由器DHCP客户端列表，如图

![image](http://7ximmr.com1.z0.glb.clouddn.com/tplink-dhcp-client.png)

那么在命令行下如何实现呢?????????

##### 步骤
* 利用firefox或chrome抓取网页发送请求

![image](http://7ximmr.com1.z0.glb.clouddn.com/tplink-dhcp-client.png)

* 利用curl模拟
<pre>
curl -s --header "Cookie:Authorization=Basic%20YWRtaW46ZXZpZGVv" http://192.168.12.1/userRpm/AssignedIpAddrListRpm.htm
</pre>
* 利用awk、sed进行后期处理