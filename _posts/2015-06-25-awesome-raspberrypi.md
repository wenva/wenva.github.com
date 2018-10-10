---
layout: post
title: "awesome-raspberrypi"
date: 2015-06-25
comments: false
categories: 树莓派
---

本文将记录我在树莓派开发过程中遇到的一些难点.

#### 无线网卡配置
* ifconfig查看是否有wlan0
<pre>
wlan0     Link encap:Ethernet  HWaddr 00:08:10:75:f0:26  
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:184 errors:0 dropped:0 overruns:0 frame:0
          TX packets:51 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:28662 (27.9 KiB)  TX bytes:8571 (8.3 KiB)
</pre>
PS: 如果有则说明驱动没问题，否则请安装相应驱动

* sudo vim /etc/wpa_supplicant/wpa_supplicant.conf
<pre>
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="你的wifi名"
psk="你的wifi密码"
proto=RSN
key_mgmt=WPA-PSK
group=CCMP TKIP
}
</pre>
* 扫描网络
<pre>
sudo iwlist wlan0 scan
</pre>
*  sudo vim /etc/network/interfaces
<pre>
auto wlan0
allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet static
address 192.168.2.111
netmask 255.255.255.0
network 192.168.2.0
gateway 192.168.2.1
</pre>
* 启动wlan0
<pre>
sudo ifup wlan0
</pre>
* ifconfig查看是否连接成功
<pre>
wlan0     Link encap:Ethernet  HWaddr 00:08:10:75:f0:26  
          inet addr:192.168.2.111  Bcast:255.255.255.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:677 errors:0 dropped:0 overruns:0 frame:0
          TX packets:67 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:83187 (81.2 KiB)  TX bytes:10637 (10.3 KiB)
</pre>
