---
layout: post
title: "Linux的NICE时间"
date: 2018-08-27
comments: false
categories: linux
---

使用top命令时，会显示一个ni值，一直没留意，今特地研究了下：NICE是指进程了优先级，从-20到19，值越高，优先级越低；NICE TIME是指NICE大于0的进程所占用CPU时间百分比

```bash
top - 14:53:27 up 58 min,  2 users,  load average: 0.22, 1.24, 1.60
Tasks: 130 total,   2 running, 124 sleeping,   4 stopped,   0 zombie
%Cpu(s):  0.0 us, 16.1 sy, 35.5 ni, 48.4 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  3877076 total,   182764 free,  3289944 used,   404368 buff/cache
KiB Swap:  2097148 total,  2096884 free,      264 used.   319240 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
10877 root      22   2  113176   1180    996 R  93.8  0.0   0:02.91 loop.sh
 6093 root      20   0  160436   7436   4368 S   6.2  0.2   2:53.93 sshd
10884 root      20   0  161972   2168   1520 R   6.2  0.1   0:00.16 top
```

PS: 从以上可以看出NICE TIME=35.5%, loop.sh进程优先级为2

进程优先级默认是继承父进程，一般为0，若要修改优先级，可以通过nice命令

```bash
# 优先级修改为2
nice -n 2 ./loop.sh

# 未指定，则修改为10
nice ./loop.sh

# 优先级修改为-2
nice -n -2 ./loop.sh
```


若要更改一个正在执行的进程

```bash
renice -n 0 10877
```