---
layout: post
title: "使用bash编写pcm转wav脚本"
date: 2017-09-26
comments: false
categories: 脚本
---

最近需要将一段pcm音频文件转换成wav，以进行播放，但没有发现类似命令，于是自己动手写了一个，现在已开源至github（https://github.com/smallmuou/wavutils）；大家知道使用c编写，难度非常小，只要填充头部44字节，并写入文件即可，我为什么用bash进行编写？这里考虑到bash脚本的几个有点：免编译、跨平台；因此对于bash脚本，可以做到「拿来即用」. 本文将只对关键技术点进行阐述，有兴趣的童鞋，可以查看源码.

* 技术点1 - 10进制转16进制

```bash
hex() {
    printf "%0$1x" $2
}
```
利用printf来实现类似c printf的功能

* 技术点2 - 获取文件大小

```bash
filesize() {  
  /bin/ls -l $1|awk '{print $5  }'
}
```
* 技术点3 - 小端显示

```bash
little_endian() {
    local i
    len=${#1}
    for (( i=$len; i>=2; i=i-2 ))
    do
        echo -n ${1:i-2:2}
    done
}
```
小端即低位显示在前，如0x1234，则显示0x34 0x12

* 技术点4 - wav转pcm

```bash
wav2pcm() {
    dd if=$1 of=$2 bs=1 skip=44 > /dev/null 2>&1
}
```
利用dd skip跳过头部44字节即可