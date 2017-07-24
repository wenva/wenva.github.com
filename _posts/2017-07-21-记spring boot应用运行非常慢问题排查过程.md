---
layout: post
title: "记spring boot应用运行非常慢问题排查过程"
date: 2017-07-21
comments: false
categories: java
---

项目上遇到一个问题『Spring Boot应用运行非常慢』，一个正常只要运行3分钟的应用在我们的自己服务器上需要运行10多分钟，针对这个问题我们做过了一些尝试

* 更换服务器（硬盘放到其他服务器运行） - 问题依旧
* 更换操作系统 - 问题不存在

根据以上，我们初步断定是运行环境的问题

于是我对CPU、Memory、IO进行了检测，发现都很正常,因此应该是java运行环境引起的。

于是我编写了java的示例程序HelloWorld，在服务器上测试，发现运行速度跟PC有一定的差别，但由于代码过简单，差别不大，当时以为是配置差别，没太多留意，于是我有编写了Spring Boot的HelloWorld，发现启动需要50s左右，而在PC上只需要5s左右，这差别也太大了；

于是我初步猜想是不是Spring Boot的那段代码block，先去Google发现大家提到的random问题，但很不幸，我更换成urandom后，问题依旧；

于是没有办法，我只能从Spring及Spring Boot源码入手，我从Github 下载了相应的源码，并编译，打印了些位置，发现基本定位不出来，因为从打印的情况看，时间不是耗在某个点，而是均匀分别，普遍偏慢；

于是我更换了策略，从java环境入手。本来要更新下jdk版本，在无意间，发现java版本号带有debug字样，如下`java -version`：

<pre>
openjdk version "1.8.0_51-debug"
OpenJDK Runtime Environment (build 1.8.0_51-debug-b16)
OpenJDK 64-Bit Server VM (build 25.51-b03-debug, mixed mode)
</pre>

于是非常惊喜，我在自己PC上确认了下，并没有带debug字样，这样想来，使用debug来运行确实会导致整体偏慢，因此我使用`alternatives --config java`将java切换到正式版，之后打印出来的信息如下：

<pre>
openjdk version "1.8.0_131"
OpenJDK Runtime Environment (build 1.8.0_131-b11)
OpenJDK 64-Bit Server VM (build 25.131-b11, mixed mode)
</pre>

于是，我重新验证了HelloWorld程序，发现速度正常了（7s左右），又验证了我们自己的应用，时间3分钟左右，至此，这个问题终于得到了解决.


### 总结

java程序慢是由于使用了debug版本的java，导致整个java运行速度偏慢.
