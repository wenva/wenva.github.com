---
layout: post
title: "论XCODE之Architectures、Valid Architectures和Build Active Architecture Only"
date: 2015-04-15
comments: false
categories: OBJC
---

对于自己不懂的东西，总想弄明白，可有时又没有那么多时间，于是可能就不了了之，就像今天要讲的"Architectures", 之前弄明白了“Build Active Architecture Only”的含义，可是对于“Architectures”和“Valid Architectures”，确是云里雾里的，今天总算抽点时间把它弄明白了.

## 1. 解释

###  Build Active Architecture Only
 这个比较简单，是指只编译当前激活的CPU架构（即当前调试的设备）

###  Architectures	 - 想
 Architectures是指你的product想编译的CPU架构

###  Valid Architectures - 能
Valid Architectures是指你能编译的CPU架构

## 2. 举例 - “理想很丰满，现实很骨感”
关于上面的阐述，大家应该就比较清楚了，这里举一个浅显的例子:
<pre>
Architectures好比“梦想”，我想当CEO、想当产品经理、想当BOSS、想当程序猿
Valid Architectures好比“现实”，可是我只能当程序猿（因为其他你都不会^_^）
那么最终结果呢，那只能当程序猿了
</pre>

## 3. 错误分析
看了上面的阐述，就能很容易地知道下面错误的原因:
<pre>
Check dependencies
No architectures to compile for (ARCHS=armv7s, VALID_ARCHS=arm64).
</pre>
上述错误可以典型的认为是“想一出，做一出”，你说能不出错嘛！！！！！关于此问题，请不要问我如何解决(就是如此任性^_^)

## 4. 综述
通过上面的描述，我想大家应该很清楚了“Architectures”与“Valid Architectures”的关系，于是这里有一个公式：

Product = Architectures 交 Valid Architectures，即最终应用程序支持的CPU架构是取“Architectures”与“Valid Architectures”的交集.
