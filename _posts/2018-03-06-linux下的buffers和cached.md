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

buffers：用于存储页、块信息，如文件属性、文件列表等
cached：用于存放文件内容

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
echo 2 > /proc/sys/vm/drop_caches
```

