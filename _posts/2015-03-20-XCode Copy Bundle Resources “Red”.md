---
layout: post
title: "XCode Copy Bundle Resources “Red”"
date: 2015-03-20
comments: false
categories: IOS
---
本文将阐述XCode Copy Bundle Resources中为何会出现红色的文件资源.

XCode -> Build Phases -> Copy Bundle Resources, Copy Bundle Resources指定了需要拷贝的资源，包括xib、png、strings等等，如果app允许后发现资源不存在，则可以到此处查看，可能会发现相应资源为红色，以前了解到的是相应资源不存在，而今天遇到一件坑爹的事，发现资源明明存在，而且重新导入还是红色，于是查了下，得到如下信息：
<pre>
In my experience with Xcode 4.6.3, the english version is required—localized resources showed red until the English localization was enabled in the resource's File inspector window.
</pre>

尝试把红色xib资源的英文localized勾选上，神奇地发现正常，真是坑啊
