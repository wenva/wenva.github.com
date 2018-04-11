---
layout: post
title: "喜马拉雅音频下载工具 - xmlyfetcher"
date: 2018-04-11
comments: false
categories: 工具
---


> xmlyfetcher用于下载喜马拉雅歌曲资源，可以下载单个音频资源，也可以下载整个专辑. 项目地址：https://github.com/smallmuou/xmlyfetcher

[![点击查看实际运行效果](http://upload-images.jianshu.io/upload_images/1415592-96cdaf4dc720a97b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)](https://asciinema.org/a/4jz6NqQIeLZL7weqpZDQ17Wi6?autoplay=1)

## 安装

1. 安装jshon

```bash
wget http://kmkeen.com/jshon/jshon.tar.gz
tar xzvf json.tar.gz
cd jshon-20120914
make
sudo make install
```
PS: jshon下载地址可能会变更，请根据官网提示下载.

2. 安装该工具

```bash
git clone https://github.com/smallmuou/xmlyfetcher.git
cd xmlyfetcher
sudo cp xmlyfetcher /usr/local/bin/
sudo chmod +x /usr/local/bin/xmlyfetcher
```

## 使用

```bash
# 下载专辑
xmlyfetcher http://www.ximalaya.com/10553948/album/260744/

# 下载单个歌曲
xmlyfetcher 76515823

# 下载到指定目录
xmlyfetcher -o ~/Downloads http://www.ximalaya.com/10553948/album/260744/
```
PS: 可以使用`xmlyfetcher -h`查看更详细的帮助

## 许可

该开源工具具有MIT许可协议. 本工具仅限个人学习，不用于商业等用途. 所涉及的音视频资源版权归喜马拉雅所有.