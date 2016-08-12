---
layout: post
title: "论linux下service的坑"
date: 2016-08-12
comments: false
categories: linux
---

近日，通过service运行脚步来跑java程序，发现输出的中文都是?，而直接运行脚步又是正常的，感觉非常奇怪，于是通过`man service`查看
<pre>
service(8)                                                          service(8)

NAME
       service - run a System V init script

SYNOPSIS
       service SCRIPT COMMAND [OPTIONS]

       service --status-all

       service --help | -h | --version

DESCRIPTION
       service runs a System V init script in as predictable environment as possible, removing most environment variables and with current working directory set to /.

       The  SCRIPT  parameter  specifies  a  System  V  init script, located in /etc/init.d/SCRIPT.  The supported values of COMMAND depend on the invoked script, service passes COMMAND and
       OPTIONS it to the init script unmodified.  All scripts should support at least the start and stop commands.  As a special case, if COMMAND is --full-restart, the script is run twice,
       first with the stop command, then with the start command.

       service --status-all runs all init scripts, in alphabetical order, with the status command.

FILES
       /etc/init.d
              The directory containing System V init scripts.

ENVIRONMENT
       LANG, TERM
              The only environment variables passed to the init scripts.

SEE ALSO
       chkconfig(8), ntsysv(8)
</pre>
其中提到`The only environment variables passed to the init scripts`，大致应该是说只传递LANG、TERM两个环境变量.猜测应该是环境变量的原因，果然通过export查看所有环境变量，并通过export引入所有变量；发现果然可以，于是逐一排查，发现是LANG没有传入，于是导入LANG，如下
<pre>
export LANG="zh_CN.UTF-8"
</pre>

### 为什么？
可是为何需要引入LANG，通过spring boot查看[启动代码](https://github.com/spring-projects/spring-boot/blob/master/spring-boot/src/main/java/org/springframework/boot/context/FileEncodingApplicationListener.java)发现如下内容
<pre>
/**
  ...
  * The System property {@code file.encoding} is normally set by the JVM in response to the
  * {@code LANG} or {@code LC_ALL} environment variables.
  ...
**/

 public class FileEncodingApplicationListener
		implements ApplicationListener<ApplicationEnvironmentPreparedEvent>, Ordered {
		...
		String encoding = System.getProperty("file.encoding");
</pre>

PS：java通过file.encoding来读取编码，而file.encoding是通过LANG来决定，详情可以参考[这里](http://www.tuicool.com/articles/Ffiy2m)