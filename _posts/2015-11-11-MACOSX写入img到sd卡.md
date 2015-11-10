---
layout: post
title: "MACOSX写入img到sd卡"
date: 2015-11-11
comments: false
categories: MACOSX
---

最近在整树莓派的声卡，又需要重新装系统，这里记录下如何将img 写入到sd卡

* 格式化
<pre>
diskutil list
sudo diskutil unmountDisk /dev/disk3
sudo newfs_msdos -F 16 /dev/disk3
</pre>
* 写入
<pre>
sudo dd if=~/Desktop/raspberrypi.dmg of=/dev/disk3
</pre>

* 卸载
<pre>
sudo diskutil eject /dev/disk3
</pre>