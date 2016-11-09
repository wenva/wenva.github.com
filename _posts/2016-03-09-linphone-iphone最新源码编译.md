---
layout: post
title: "linphone-iphone最新源码编译"
date: 2016-03-09
comments: false
categories: iOS
---

最近在解决音视频对讲的问题，发现原先那版linphone sdk存在比较多的问题，比如内存泄露、信令错乱、crash等等，通过github了解到，linphone sdk一直都在更新，于是想更新下linphone sdk. 

## clone
编译代码之前，肯定是先clone最新代码
<pre>
git clone https://github.com/BelledonneCommunications/linphone-iphone --recursive
</pre>
更新完后发现跟原来的编译方式有了比较大的区别，更新完后编译步骤更清晰，更方便. 可以执行./prepare.py --help 查看帮助

## config
开始配置前，请使用`./prepare.py -c`清理上一次编译结果

#### 架构

目前linphone支持arm64、armv7、i386、x86_64架构，大家可以自行选择，一般只要armv64、armv7就行了，命令如下:
<pre>
./prepare.py arm64 armv7
</pre>

#### 特性

可以通过`./prepare.py -lf`来查看特性开关，若不想编译哪个模块，设为OFF，如我不需要编译MKV模块，就执行如下命令
<pre>
./prepare.py -DENABLE_MKV=ON arm64 armv7
</pre>

## build sdk
config后，执行make进行编译
<pre>
make
</pre>
若在编译过程中，遇到`GNU assembler not found, install/update gas-preprocessor`记得更新gas-preprocessor
<pre>
wget --no-check-certificate https://raw.githubusercontent.com/FFmpeg/gas-preprocessor/master/gas-preprocessor.pl && chmod +x gas-preprocessor.pl && sudo mv gas-preprocessor.pl /usr/local/bin
</pre>
PS: 不要去下载https://github.com/yuvi/gas-preprocessor这个，可能是比较旧；更新完后，记得将`/usr/local/bin`添加到PATH环境变量中
<pre>
export PATH=/usr/local/bin:$PATH
</pre>

## build app
编译完后sdk就可以开始编译app了，用xcode打开linphone.xcodeproj，更改证书，直接编译



