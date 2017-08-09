---
layout: post
title: "linux内核module编译"
date: 2017-08-08
comments: false
categories: linux
---

最近公司服务器系统升级至 centos7，升级后发现原先的 bios 升级工具无法使用，提示:

```
ERROR : driver "amifldrv" not found
rmmod: ERROR: Module amifldrv_mod is not currently loaded
ERROR : driver "amifldrv" not found
rmmod: ERROR: Module amifldrv_mod is not currently loaded
ERROR : Unable to load driver.
10 - Error: Unable to load driver.
```
下面简单描述下解决过程：

1. 下载对应版本linux内核源码（uname -r）
2. 将源码拷贝至/usr/src/kernels目录下
3. 进入源码目录,依次执行`make oldconfig && make prepare && make scripts && make vmlinux`
4. 下载[amifldrv源码](!https://github.com/mrwnwttk/afulnx)
5. 执行 make default，之后会生成.o文件
6. 执行insmod .o，如果没有报错，则表示模块编译成功


以上是我编译内核 module 的大致经过，中间遇到了很多坑，比如没有`make vmlinux`导致"no symbol version for struct_module"。
