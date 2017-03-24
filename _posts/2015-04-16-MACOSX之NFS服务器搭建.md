---
layout: post
title: "MACOSX之NFS服务器搭建"
date: 2015-04-16
comments: false
categories: APPLE
---

NFS即网络文件系统，允许一个系统在网络上与它人共享目录和文件，通过mount可以将它挂载点本地节点，就可以方便访问远程文件. MACOSX如何搭建NFS服务器呢？

1. 编辑exports
	<pre>
	sudo vi /etc/exports
	
	/Users -network 192.168.0.0 -mask 255.255.0.0
</pre>

2. 启用nfsd
	<pre>
	sudo nfsd enable
	</pre>
3. 测试验证
	<pre>
	showmount -e
	</pre>
