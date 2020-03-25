---
layout: post
title: "命令行下获取TP-LINK路由器DHCP客户端列表"
date: 2016-02-04
comments: false
categories: SHELL
---

需要实现一个需求：当我回到家时，音乐自动播放起来；关于这个需求有很多方式，比如声音识别、摄像头识别（仿生），当然也可以通过蓝牙、WIFI。声音与摄像识别的难度相对较大，后期再研究，因此就剩下蓝牙和WIFI，蓝牙的话，目前缺少蓝牙适配器，因此也暂时不考虑，那么就剩下WIFI了. 这里讲下总体思路，就是实时监控路由器中是否有我的手机在线，如果在线，则认为我在家. 那么问题就来了，如何知道我手机是否连到路由器. 这里有两个方法，方法一：为手机设置静态ip，不断ping这个ip；方法二：动态获取手机ip，不断ping这个ip.本文主要讲述如何动态获取手机ip.

### 尝试1
希望利用arp命令获取手机的ip，通过`arp -a`会得到如下结果：
<pre>
bogon (192.168.12.1) at d0:c7:c0:8a:1a:7c on en0 ifscope [ethernet]
bogon (192.168.12.104) at (incomplete) on en0 ifscope [ethernet]
? (192.168.12.255) at (incomplete) on en0 ifscope [ethernet]
...
</pre>
PS：通过比对MAC地址判断哪个是我的手机，但是发现个问题，`arp -a`只能查看局域网内我电脑通信过的ip信息，对于未通信的终端是没有相应信息的，因此不一定能够获取到我手机的ip，而且还发现MAC地址有时是无法获取到，如上显示incomplete

### 尝试2
通过web方式查看路由器DHCP客户端列表，如图

![image](http://7ximmr.com1.z0.glb.clouddn.com/tplink-dhcp-client.png)

那么在命令行下如何实现呢?????????

##### 步骤
* 利用firefox或chrome抓取网页发送请求

![image](http://7ximmr.com1.z0.glb.clouddn.com/tplink-dhcp-client-catch.png)

* 利用curl模拟
<pre>
curl -s --header "Cookie:Authorization=Basic%20YWRtaW46ZXZpZGVv" http://192.168.12.1/userRpm/AssignedIpAddrListRpm.htm
</pre>
PS: Authorization后是密码信息，规则是: escape("Basic "+base64("admin:"+password))，javascript代码如下
<pre>
...
var password = $("pcPassword").value;	
var auth = "Basic "+Base64Encoding("admin:"+password);
document.cookie = "Authorization="+escape(auth)+";path=/";
...
</pre>
PS: 可以使用base64在命令行下进行编码，但要注意换行符，比如`echo "evideo" | base64`，此时将编码`evideo+换行`,需要使用`echo -n "evideo" | base64`
* 利用awk、sed进行后期处理
<pre>
curl -s --header "Cookie:Authorization=Basic%20YWRtaW46ZXZpZGVv" http://192.168.12.1/userRpm/AssignedIpAddrListRpm.htm|sed -n -e "/DHCPDynList/,/)/p"|sed '1d;$d'
</pre>
通过上面的curl得到如下结果:
<pre>
"eVideos-Mini", "A8-20-66-4A-CB-B6", "192.168.12.101", "01:18:48", 
"android-6ca5b9c4644c86ec", "34-23-BA-67-ED-C6", "192.168.12.149", "01:58:49", 
...
</pre>
* 获取对应的客户端ip，并进行ping，ping通的话表示在线，否则表示不在线
<pre>
curl -s --header "Cookie:Authorization=Basic%20YWRtaW46ZXZpZGVv" http://192.168.12.1/userRpm/AssignedIpAddrListRpm.htm|awk -F[\ ,] '/smallmuou/{print $5}'|sed 's/"//g'|xargs ping -c 3
</pre>
PS：smallmuou是我的手机名

当我手机在线会得到如下信息：
<pre>
PING 192.168.12.109 (192.168.12.109): 56 data bytes
64 bytes from 192.168.12.109: icmp_seq=0 ttl=64 time=810.294 ms
64 bytes from 192.168.12.109: icmp_seq=1 ttl=64 time=26.548 ms
64 bytes from 192.168.12.109: icmp_seq=2 ttl=64 time=185.024 ms
</pre>

当我手机不在线会得到如下信息：
<pre>
PING 192.168.12.109 (192.168.12.109): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
</pre>

### 后续工作
以上已经讲出了本文的所有内容，对于本文开头提出的需求，这里还有个坑，由于iPhone手机在休眠情况下，也是ping不通的，因此需要通过加上额外的信息才能保证此方式的可行性，比如时间信息.
