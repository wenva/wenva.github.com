---
layout: post
title: "linux下的buffers和cached"
date: 2018-03-06
comments: false
categories: 运维
---

使用free命令经常看到buffers/cached占用了大量内存，那buffers/cached到底存了哪些内容？

```bash
[root@iZ94fgpisuuZ ~]# free
             total       used       free     shared    buffers     cached
Mem:       8058056    3799232    4258824          0       6704      66812
-/+ buffers/cache:    3725716    4332340
Swap:            0          0          0
```

##### 区别

* buffers：用于存储页、块信息，如文件属性、inode等；通过find查找的结果会缓存至buffers
* cached：用于存放文件内容，包括了tmpfs、共享内存、nmap等；打开一个大文件，文件内容会缓存到cached

##### 清除方法

* 清除cached
```bash
echo 1 > /proc/sys/vm/drop_caches
```

* 清除buffers
```bash
echo 2 > /proc/sys/vm/drop_caches
```

* 同时清除cached和buffers
```bash
echo 3 > /proc/sys/vm/drop_caches
```

##### 哪些情况无法清除

* tmpfs中，文件未删除，则cached无法释放
* 共享内存未释放，则cached无法释放
* nmap映射的内存未释放，则cached无法释放

