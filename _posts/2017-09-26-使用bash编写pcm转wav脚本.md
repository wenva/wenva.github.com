---
layout: post
title: "使用bash编写pcm转wav脚本"
date: 2017-09-26
comments: false
categories: 脚本
---

最近需要将一段pcm音频文件转换成wav，以进行播放，但没有发现类似命令，于是自己动手写了一个，现在已开源至github（https://github.com/smallmuou/pcm2wav）；大家知道使用c编写，难度非常小，只要填充头部44字节，并写入文件即可，我为什么用bash进行编写？这里考虑到bash脚本的几个有点：免编译、跨平台；因此对于bash脚本，可以做到「拿来即用」，本文将对几个关键技术点进行阐述.