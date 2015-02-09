---
layout: post
title: "Linphone之BelleSip"
date: 2015-02-06
comments: false
---
# Linphone之BelleSip
February 6, 2015

## 初始化SOCKET并监听端口(UDP)
<pre>
linphone_core_set_sip_transports(linphone/coreapi/linphonecore.c) -> apply_transports(linphone/coreapi/linphonecore.c) -> sal_listen_port(linphone/coreapi/bellesip_sal/sal_impl.c) -> sal_add_listen_port(linphone/coreapi/bellesip_sal/sal_impl.c) -> belle_sip_stack_create_listening_point(sipstack.c) -> belle_sip_udp_listening_point_new(udp_listeningpoint.c) -> belle_sip_udp_listening_point_init(udp_listeningpoint.c) -> belle_sip_listening_point_init 
</pre>
PS: 目前支持TCP、UDP、TLS（安全传输层协议）三种传输

* SSL与TLS
	* SSL - 位于应用层与协议层之间
	* TLS - 位于应用程序之间，可以理解为应用层

## 数据接收及处理
<pre>
on_udp_data -> 
</pre>

