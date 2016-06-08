---
layout: post
title: "理解Git的Rebase"
date: 2016-06-07
comments: false
categories: Git
---

今天同事偶然问道`git rebase`的问题，于是想去了解下，可是看了好几篇文章都无法理解，后来理解了下rebase的词面意思，rebase可以理解为重新定义起点，可以结合下图理解：

![image](http://gitbook.liuhui998.com/assets/images/figure/rebase3.png)

经过`git rebase`后，mywork分支的起点从C2切换到C4.