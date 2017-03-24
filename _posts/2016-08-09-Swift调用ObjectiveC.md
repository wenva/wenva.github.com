---
layout: post
title: "Swift调用ObjectiveC"
date: 2016-08-09
comments: false
categories: OBJC
---

Swift中调用OC代码，并不是直接import头文件，然后开始调用，而是需要进行配置，方法也很简单，步骤如下：

* 步骤一：添加Objective-C Bridging Header
<pre>
TARGET -> Swift Compiler - Code Generation -> Objective-C Bridging Header 添加头文件
</pre>

* 步骤二：调用代码
<pre>
NSLog("你好".translatorToPinYinFirstAscii()); //此处不能使用OC的中括号写法
</pre>
