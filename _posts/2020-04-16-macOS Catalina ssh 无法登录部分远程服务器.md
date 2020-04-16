---
layout: post
title: "macOS Catalina ssh 无法登录部分远程服务器"
date: 2020-04-16
comments: false
categories: 其他
---

由于近期需要升级xcode，被迫升级了macOS系统至Catalina，升级完后发现有些远程服务器服务登录，利用-v看了下

```bash
smou:Projects $ /usr/bin/ssh -v server-ip
OpenSSH_8.1p1, LibreSSL 2.7.3
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 47: Applying options for *
debug1: Connecting to server-ip port 22.
```

网上找了下其他博文，说是OpenSSH_8.1的问题（猜测应该是BUG），于是看下了相应的版本信息

```bash
smou:Projects $ /usr/bin/ssh -V
OpenSSH_8.1p1, LibreSSL 2.7.3
```

说是升级至OpenSSH_8.2就ok，而利用brew只能升到8.1，于是只能采用手动方法，步骤如下：

* 下载编译openssl

```bash
wget https://www.openssl.org/source/openssl-1.1.1f.tar.gz
tar xzvf openssl-1.1.1f.tar.gz
cd openssl-1.1.1f
./config
make
make install
```

* 下载编译openssh

```bash
wget https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-8.2p1.tar.gz
tar xzvf openssh-8.2p1.tar.gz
cd openssh-8.2p1
autoreconf
./configure
make
make install
```
PS: 需要先编译安装openssl否则会报`has no source of random numbers`的错误。

ssh会安装至`/usr/local/bin/ssh`，我们查看其版本信息

```bash
smou:Projects $ /usr/local/bin/ssh -V
OpenSSH_8.2p1, OpenSSL 1.1.1f  31 Mar 2020
```

于是试了下之前无法ssh远程登录的服务器，发现可以正常使用了。

