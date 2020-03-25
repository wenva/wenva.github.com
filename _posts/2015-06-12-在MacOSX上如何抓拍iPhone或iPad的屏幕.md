---
layout: post
title: "在MacOSX上如何抓拍iPhone或iPad的屏幕"
date: 2015-06-12
comments: false
categories: SHELL
---

今天看到iTool有一个LiveDesktop的东东，感觉挺新奇的. 于是想看看是什么原理，找了半天，发现一个好东西[libimobiledevice](https://github.com/libimobiledevice/libimobiledevice)，这个开源库提供很多工具，比如查看设备信息、设备DEBUG信息，大家可以直接编译生成这个工具，当然也可以到[这里](https://github.com/benvium/libimobiledevice-macosx)下载编译好的可执行文件.

<pre>
git clone https://github.com/benvium/libimobiledevice-macosx
cd libimobiledevice-macosx
export DYLD_LIBRARY_PATH=.:$DYLD_LIBRARY_PATH 
./idevicescreenshot -u 690a505acd5ea06233a2c10c173907c135070ace
</pre>
执行上述命令后，可以在当前路径下生成screenshot-xxx.tiff

### 编译libimobiledevice
<pre>
sudo brew install usbmuxd
git clone https://github.com/libimobiledevice/libimobiledevice
cd libimobiledevice
./autogen.sh
make
make install
</pre>

#### 展望
我稍微查看了下抓拍的原理，是往usb发送相应的指令，并接收图片数据. 后续会继续了解libimobiledevice相关的代码.


