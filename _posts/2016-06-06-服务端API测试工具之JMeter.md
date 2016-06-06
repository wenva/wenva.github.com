---
layout: post
title: "服务端API测试工具之JMeter"
date: 2016-06-06
comments: false
categories: API
---

在互联化的时代浪潮里，服务端API变得无处不在，几乎每个公司都有会提供服务API给第三方调用，而服务API的测试也就提上日程，本文我们将介绍API测试工具JMeter，[JMeter](http://jmeter.apache.org)是Apache组织的开放源代码项目，它是功能和性能测试的工具. 本文将对Jmeter进行比较系统化的阐述.

## 1. 概述
对于服务端API的测试，我们自然而然地想到，"发请求收回复"，因此想curl、postman都可以实现类似的功能，但面对批量性、关联性、压力测试等需求时，就显得不足，或者说无法完成，那么有没有一款软件能够实现呢？经过查找，发现了JMeter，[JMeter](http://jmeter.apache.org)是Apache组织的开放源代码项目，它是功能和性能测试的工具. 它包含了线程组、定时器、断言、元件、前缀处理器、后置处理器、监听器等，可以说功能非常强大. 下面我JMeter涉及到的一些词语进行描述:

* 测试计划 - 根节点，可以理解为工程，其中配置了工程的基础信息，如jar包、各线程组运行机制等.一个测试计划可以包含多个线程组.
* 线程组 - 也可以称为用户组，指一组测试用例
* 逻辑控制器 - 对测试单元的逻辑控制，包含循环、随机等
* 配置元件 - 公共单元，如默认HTTP请求头、Cookie等
* 定时器 - 各个测试用例的调用顺序
* 前置处理器 - 在测试用例执行前预处理
* Sampler - 采样器，具体的测试用例，包含FTP请求、HTTP请求
* 后置处理 - 在测试单元执行后对结果的处理
* 断言 - 对结果进行预定化验证
* 监听器 - 输出并分析结果

## 2. 安装
* 进入[JMeter下载界面](http://jmeter.apache.org/download_jmeter.cgi)，下载相应版本JMeter，由于JMeter是利用Java实现的，因此需要先安装Java环境.
* 解压压缩包，并进入目前
* 类Unix请执行`jmeter.sh`，Windows用户请执行`jmeter.bat`

## 3. DEMO
本例将以授权接口作为测试用例.

* 添加【线程组】
<pre>
右键【测试计划】-> 添加 -> Threads(Users) -> 线程组
</pre>
* 添加【HTTP请求默认值】
<pre>
右键【线程组】-> 添加 -> 配置元件 -> HTTP请求默认值
</pre>
PS: 填写API请求的域名、端口等公共信息
* 添加【HTTP信息头管理器】
<pre>
右键【线程组】-> 添加 -> 配置元件 -> HTTP信息头管理器
</pre>
PS: 填写API请求头公共信息，如Content-Type:application/json等
* 添加【察看结果树】
<pre>
右键【线程组】-> 添加 -> 监听器 -> 察看结果树
</pre>
* 添加【HTTP请求】
<pre>
右键【线程组】-> 添加 -> Sampler -> HTTP请求
</pre>


