---
layout: post
title: "Unix无法执行bash_profile"
date: 2017-04-20
comments: false
categories: 运维
---

一些理所当然的事，一旦出错，我们就如同热锅上的蚂蚁，到处乱窜，没有任何方向，因为在我们的脑海里，这是再熟悉不过的，是不可能发生的。就如同前些时间遇到的问题：MacOSX上Terminal登录的时候不执行bash_profile。遇到这种情况，必须clear自己，清空固化在脑中的「所谓常识」，理清原理。


其实针对这个问题，我们忽略了只有bash才会执行bash_profile，而其实shell出来bash，还有dash、sh、zsh等等，它们各自执行自己的profile.

最后来点不重要的: MacOSX下如何修改shell ?

```
chsh -s /bin/bash
```
