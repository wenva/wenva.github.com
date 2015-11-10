---
layout: post
title: "利用dSYM文件分析crash"
date: 2015-11-10
comments: false
categories: iOS
---

最近使用了蒲公英的SDK来管理crash信息，但是有个问题是发现上传的crash信息显示一堆数字 0x00000001823bcf48、... 着实痛苦，后面查了下可以利用dSYM来配合分析，本文将讲述其分析过程.

#### 1. command line tools
<pre>
 xcode-select --install
</pre>

#### 2. 