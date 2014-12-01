---
layout: post
title: "Linphone-IOS源码编译"
date: 2014-11-20
comments: false
---
# Linphone-IOS源码编译
2014-11-20

## 下载源码包
* 
	<pre>git clone git://git.linphone.org/linphone-iphone.git --recursiv </pre>

## 安装依赖库
* 依赖库
	<pre>
$ sudo port install coreutils automake autoconf libtool intltool wget pkgconfig cmake gmake yasm nasm grep doxygen ImageMagick optipng antlr3 </pre>

* gas-preprosessor.pl - ffmpeg编译
	<pre>
$ wget --no-check-certificate https://raw.github.com/yuvi/gas-preprocessor/master/gas-preprocessor.pl
$ sudo mv gas-preprocessor.pl /opt/local/bin/.
$ sudo chmod +x /opt/local/bin/gas-preprocessor.pl</pre>
* Link
	<pre>
$ sudo ln -s /opt/local/bin/glibtoolize /opt/local/bin/libtoolize
$ sudo ln -s  /usr/bin/strings /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/usr/bin/strings</pre>

## 编译SDK