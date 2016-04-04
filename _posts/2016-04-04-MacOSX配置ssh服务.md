---
layout: post
title: "MacOSX配置ssh服务"
date: 2016-04-04
comments: false
categories: MacOSX
---

最近想用公司的一台闲置的Mac-Mini搭建一个服务器，而Mac-Mini没有显示器，因此想通过ssh来登录并进行操作，本文将讲述MacOSX系统如何配置ssh服务.

### sshd

幸运的是，系统已集成sshd命令，大家可以执行下sshd命令，但发现会报出如下错误.

<pre>
StarnetdeMacBook-Pro:weiju-sdk-docs starnet$ sshd
sshd re-exec requires execution with an absolute path
</pre>

含义就是sshd需要绝对路径执行，于是我们使用`which sshd`查看绝对路径，并执行

<pre>
StarnetdeMacBook-Pro:weiju-sdk-docs starnet$ which sshd
/usr/sbin/sshd
StarnetdeMacBook-Pro:weiju-sdk-docs starnet$ /usr/sbin/sshd
Could not load host key: /etc/ssh/ssh_host_rsa_key
Could not load host key: /etc/ssh/ssh_host_dsa_key
Could not load host key: /etc/ssh/ssh_host_ecdsa_key
Could not load host key: /etc/ssh/ssh_host_ed25519_key
StarnetdeMacBook-Pro:weiju-sdk-docs starnet$ 
</pre>

可是又报出Could not load host key错误. 解决方法:

<pre>
sudo ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
</pre>

再执行

<pre>
StarnetdeMacBook-Pro:weiju-sdk-docs starnet$ sudo /usr/sbin/sshd
StarnetdeMacBook-Pro:weiju-sdk-docs starnet$ ps -e|grep sshd
74801 ??         0:00.00 /usr/sbin/sshd
74859 ttys001    0:00.00 grep --color sshd
</pre>
自此ssh服务已启动，可以通过`ssh username@ip`进行测试