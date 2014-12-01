---
layout: post
title: "Asterisk 技术点"
date: 2014-11-07
comments: true
---
# Asterisk 技术点

* brew install apple-gcc-4.2
* ./configure CC=gcc-4.2
* define RONLY 0x1


Q:process_sdp: ignoring 'video' media offer because port number is zero

A:说明视频编码不支持，core show codecs video查看支持的视频编码（linphone默认只支持vp8）

## NAT类型
[NAT分类](http://blog.163.com/hlz_2599/blog/static/1423784742012317102533915/)

## Linphone
###### Stun Server
当设置Stun Server后, Linphone会获取从Stun Server获取到公网IP和port，并在发送SIP时填充Contact，当没有设置时，则Asterisk会返回，填写Recieved和rport
<pre>
12:34:24.516868 IP xuwenfas-iPhone.63627 > 192.168.60.151.5060: SIP, length: 411
Eh...?..@..$......<.........REGISTER sip:192.168.60.151 SIP/2.0
Via: SIP/2.0/UDP 192.168.1.131:63627;branch=z9hG4bK.PcrNcrd8a;<font color="00ff00">rport</font>
From: < sip:112@192.168.60.151>;tag=~wyqkEm4k
To: sip:112@192.168.60.151
CSeq: 20 REGISTER
Call-ID: QuDP68~7EC
Max-Forwards: 70
Supported: outbound
Contact: < sip:112@192.168.1.131:63627>;+sip.instance="< urn:uuid:f402ede7-9815-42d5-b0c5-66d7dabf93ba>"
Expires: 3600
User-Agent: (belle-sip/1.3.3)


12:34:24.518448 IP 192.168.60.151.5060 > xuwenfas-iPhone.63627: SIP, length: 530
E.......?..E..<............OSIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.1.131:63627;branch=z9hG4bK.PcrNcrd8a;<font color="00ff00">received=192.168.60.147;rport=63627</font>
From: < sip:112@192.168.60.151>;tag=~wyqkEm4k
To: sip:112@192.168.60.151;tag=as16758747
Call-ID: QuDP68~7EC
CSeq: 20 REGISTER
Server: Asterisk PBX SVN-trunk-r423130
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, SUBSCRIBE, NOTIFY, INFO, PUBLISH, MESSAGE
Supported: replaces, timer
Expires: 3600
Contact: < sip:112@192.168.1.131:63627>;expires=3600
Date: Tue, 18 Nov 2014 00:25:29 GMT
Content-Length: 0


12:34:25.381597 IP xuwenfas-iPhone.63627 > 192.168.60.151.5060: SIP, length: 433
Eh......@..x......<.........REGISTER sip:192.168.60.151 SIP/2.0
Via: SIP/2.0/UDP 192.168.1.131:63627;branch=z9hG4bK.~kn9Nn2n7;rport
From: <sip:112@192.168.60.151>;tag=hQmZSm18L
To: sip:112@192.168.60.151
CSeq: 20 REGISTER
Call-ID: nPk8A34HWK
Max-Forwards: 70
Supported: outbound
<font color="00ff00">Contact: < sip:112@192.168.60.147:63627></font>;+sip.instance="< urn:uuid:f402ede7-9815-42d5-b0c5-66d7dabf93ba>"
Expires: 3600
User-Agent: LinphoneIPhone/2.2.3 (belle-sip/1.3.3)

</pre>

## rport
获得IP地址是在Via头中带上received参数。为了得到端口信息，也参考了这种方式，即在Via头中带上rport属性来指明端口信息。

如果是支持rport机制的服务器，它需要在接收到的请求中检查Via头是否包含一个没有值的rport参数。如果有，它需要在回应中带上rport的值，这与received的处理类似。
<pre>
12:09:59.566063 IP xuwenfas-iPhone.61710 > 192.168.60.151.5060: SIP, length: 433
Eh......@..I......<.......z.REGISTER sip:192.168.60.151 SIP/2.0
Via: SIP/2.0/UDP 192.168.1.131:61710;branch=z9hG4bK.ccoKJW05t;rport
From: <sip:112@192.168.60.151>;tag=CDqPrLUqI
To: sip:112@192.168.60.151
CSeq: 24 REGISTER
Call-ID: 81nl08JxWA
Max-Forwards: 70
Supported: outbound
Contact: <sip:112@192.168.60.147:61710>;+sip.instance="<urn:uuid:f402ede7-9815-42d5-b0c5-66d7dabf93ba>"
Expires: 3600
User-Agent: LinphoneIPhone/2.2.3 (belle-sip/1.3.3)


12:09:59.567578 IP 192.168.60.151.5060 > xuwenfas-iPhone.61710: SIP, length: 531
E../....?..N..<...........s/SIP/2.0 200 OK
Via: SIP/2.0/UDP 192.168.1.131:61710;branch=z9hG4bK.ccoKJW05t;received=192.168.60.147;rport=61710
From: <sip:112@192.168.60.151>;tag=CDqPrLUqI
To: sip:112@192.168.60.151;tag=as4b4f12a7
Call-ID: 81nl08JxWA
CSeq: 24 REGISTER
Server: Asterisk PBX SVN-trunk-r423130
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, SUBSCRIBE, NOTIFY, INFO, PUBLISH, MESSAGE
Supported: replaces, timer
Expires: 3600
Contact: <sip:112@192.168.60.147:61710>;expires=3600
Date: Tue, 18 Nov 2014 00:01:04 GMT
Content-Length: 0

</pre>

## SIP.conf
* autocreatepeer=yes 允许自动创建节点
* context=xx，指定拨号规则（定义在extension.conf中）
* directmedia 见canreinvite
* directrtpsetup
* canreinvite 重定向媒体流，在1.6.2后改为directmedia
	* yes - allow RTP media direct
	```This means that this SIP is _always_ able to receive direct RTP media,from any other peer, regardless of IP address or network route.```
	* no - deny re-invites(转发)
	```This means that this SIP peer is not able to receive direct RTP media,from any other peer, regardless of IP address or network route.```
	* nonat - allow reinvite when local, deny reinvite when NAT
	* update - use UPDATE instead of INVITE
	* update,nonat - use UPDATE when local, deny when NAT
	
* allow 允许编解码器
* allowguest 允许来电
* media_address 设定媒体流地址
* externip - 外网IP，与localnet配合用，当呼入的ip与localnet不在同一个网段，则用externip替换sdp中的ip
* localnet=192.168.2.0/255.255.255.0。。。可以有多个localnet（多网卡情况）
* nat
	* yes - forces RFC 3581 behavior and enables symmetric RTP support
	* no - only enables RFC 3581 behavior if the remote side requests it and disables symmetric RTP support
	* force_rport -  forces RFC 3581 behavior and disables symmetric RTP support
	* comedia - enables RFC 3581 behavior if the remote side requests it and enables symmetric RTP support.
	
	* force_rport+comedia = yes

## UPDATE
SIP的UPDATE（[RFC3311](https://tools.ietf.org/html/rfc3311)）消息是SIP扩展的一种机制，用以在通话尚未建立的时候更新媒体流状态的一种机制。

INVITE --- UPDATE --- REINVITE

## 会话流程
```When SIP initiates the call, the INVITE message contains the information on where to send the media streams. Asterisk uses itself as the end-points of media streams when setting up the call. Once the call has been accepted, Asterisk sends another (re)INVITE message to the clients with the information necessary to have the two clients send the media streams directly to each other.```

理解: 当SIP发起会话时，INVITE通过SDP携带媒体流传输需要的信息（IP、PORT），Asterisk会将自己作为媒体流接受者，一旦邀请被接受，Asterisk会发送带有媒体流信息的(re)INVITE给客户端，以便客户端之间建立P2P连接.
当以下条件不会发送(re)INVITE:

* canreinvite=NO
* 客户端使用不同的编解码器
* Dial包含 ''t'', ''T", "h", "H", "w", "W" or "L" (with multiple arguments) 