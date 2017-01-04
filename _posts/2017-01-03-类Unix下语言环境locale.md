---
layout: post
title: "类Unix下语言环境locale"
date: 2017-01-03
comments: false
categories: unix
---

引言：在使用类Unix系统时，经常会遇到无法显示中文字符，各种乱码，于是Google，找到了若干解决方案，各种设置LC_CTYPE、或者LC_ALL、又或者LANG，然后经过多种答案的叠加，问题就解决，可对其中的原理仍无法理解，可能每次遇到乱码的情况还不一样，解决方法也不一样，于是就更晕.我最近也遇到关于中文字符显示成？，于是想更深入的了解下，找到了一篇[好文](http://www.cnblogs.com/xlmeng1988/archive/2013/01/16/locale.html)，现在我再整理下.

## 1. 风俗(locale)

在人类的世界里，不同地域的人有着不同的风俗，而计算机是给人用的，那自然也要遵循着这一套规则，而这套规则就是locale，我们执行下`locale`命令：

```
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
```

## 2. 表示
『我说中文，国籍是中华人民共和国，使用国标2312字符集来表达字符』这是我的介绍，locale表示方法类似，格式如下：

<pre>
语言[_地域[.字符集]]
</pre>
如：zh_CN.GB2312

可以使用`locale -a`来查看系统支持的所有字符集. 如果字符集缺省，则采用默认值，可以通过`locale -v -a`查看，如
<pre>
locale: zh_CN           archive: /usr/lib/locale/locale-archive
-------------------------------------------------------------------------------
    title | Chinese locale for Peoples Republic of China
    email | bug-glibc-locales@gnu.org
 language | Chinese
territory | P.R. of China
 revision | 0.1
     date | 2000-07-25
  codeset | GB2312

...

locale: zh_CN.gb2312    archive: /usr/lib/locale/locale-archive
-------------------------------------------------------------------------------
    title | Chinese locale for Peoples Republic of China
    email | bug-glibc-locales@gnu.org
 language | Chinese
territory | P.R. of China
 revision | 0.1
     date | 2000-07-25
  codeset | GB2312
</pre>
PS: zh_CN与zh_CN.gb2312是等价的

## 3. 分类(Categories)
风俗可能会包含各方各面，比如吃什么、做什么等等. 而locale同样包含着各个分类，从上面的结果可以看出其包含12个分类(LC_前缀)

* LC_CTYPE - 用于字符分类和字符串处理，控制所有字符的处理方式，包括字符编码，字符是单字节还是多字节，如何打印
* LC_NUMERIC - 数字格式，如小数点、千分位各是什么字符
* LC_TIME - 时间格式，如星期、月、上午、下午怎么表示
* LC_MESSAGES - 消息格式，如『肯定』、『否定』怎么表示，另外还有一个LANGUAGE参数，它与LC_MESSAGES相似，但如果该参数一旦设置，则LC_MESSAGES参数就会失效。LANGUAGE参数可同时设置多种语言信息，如LANGUANE="zh_CN.GB18030:zh_CN.GB2312:zh_CN"
* LC_PAPER - 纸张大小，如长、宽多少
* LC_TELEPHONE - 电话号码格式，如区号，显示格式
* LC_NAME - 名字格式，如miss用『小姐』表示，mr用『先生』表示等
* LC_ADDRESS - 地址格式，如国家、城市等
* LC_MEASUREMENT - 度量格式
* LC_IDENTIFICATION - 该locale的概述
* LC_MONETARY - 货币格式，如￥、小数点、千分位
* LC_COLLATE - 排序规则

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

## 4. 改进
有了以上的locale及categories就能满足了【不同地域不同风俗】的需求，但考虑到方便性，系统又引入LC_ALL、LANG这两个环境变量

* LC_ALL - 全局设定
* LANG - 默认设定

有了以上两个值，于是又引入了如下规则

* 规则一：优先级：`LC_ALL > LC_* > LANG`
* 规则二：如果LC_ALL、LC_*、LANG都不指定，则采用POSIX作为locale，即 C locale

## 5. 总结
有了以上背景，应该就能比较好地了解Unix/Linux的语言环境，其中最重要的三个是：LANG、LC_CTYPE、LC_ALL

