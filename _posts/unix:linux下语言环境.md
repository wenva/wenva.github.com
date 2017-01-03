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
风俗可能会包含各方各面，比如吃什么、做什么等等. 而locale同样包含着各个分类，从上面的结果可以看出其包含12个分类(LC_前缀)

* LC_CTYPE
* LC_NUMERIC - 数字格式，如小数点、千分位各是什么字符
* LC_TIME - 时间格式，如星期、月、上午、下午怎么表示
* LC_MESSAGES - 消息格式，如『肯定』、『否定』怎么表示
* LC_PAPER - 纸张大小，如长、宽多少
* LC_TELEPHONE - 电话号码表示，如区号，显示格式
* LC_NAME - 姓名表示，如
* 

具体定义可以到/usr/share/i18n/locates/下对应的文件查看，其中字符采用UNICODE16表示，如zh_CN文件

```
...

LC_NUMERIC
decimal_point             "<U002E>"    小数点用.表示
thousands_sep             "<U002C>"    千分位用,表示
grouping                  3
END LC_NUMERIC

LC_TIME
abday 	"<U65E5>";"<U4E00>";"<U4E8C>";"<U4E09>";"<U56DB>";"<U4E94>";"<U516D>"  星期缩写：日、一、二、三、四、五、六

day 	"<U661F><U671F><U65E5>";/   星期日
	"<U661F><U671F><U4E00>";/		星期一
...
```

## 