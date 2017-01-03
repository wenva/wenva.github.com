---
layout: post
title: "Unix/Linux下语言环境"
date: 2017-01-03
comments: false
categories: Unix
---

引言：在使用Linux系统时，经常会遇到无法显示中文字符，各种乱码，于是Google，找到了若干解决方案，如需要设置LC_CTYPE、或者LC_ALL、又或者LANG，然后经过多种答案的叠加，问题就解决，可对其中的原理仍无法理解，于是每次遇到乱码，每次都得重新来过一遍，我最近也遇到此情况，于是想更深入的了解下，找到了一篇[好文](http://www.cnblogs.com/xlmeng1988/archive/2013/01/16/locale.html)，现在我再整理下.

## 风俗(locale)

在人类的世界里，不同地域的人有着不同的风俗，而计算机是给人用的，那自然也要遵循着这一套规则，而这套规则就是locale，我们执行下`locale`命令：

<pre>
smallmuou:locales $ locale
LANG=en_US.UTF-8
LC_CTYPE=zh_CN.utf8
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=
</pre>

## 分类(Categories)
风俗可能会包含各方各面，比如可以吃什么、不可以吃什么、可以干什么、不可以什么等等. 而locale同样包含着各个子项目，从上面的结果也可以看出(LC_前缀)

* LC_CTYPE