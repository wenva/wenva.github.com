---
layout: post
title: "sed n,N,p,P,d,D区别"
date: 2018-07-16
comments: false
categories: Linux
---

```
n - 读入下一行，且只将第二行加入模式空间，即后续命令只对第二行生效
N - 读入第二行，把两行当做一行处理
p - 打印模式空间内所有行
P - 只打印第一行
d - 删除模式空间内所有行
D - 只删除第一行
```

示例

* n vs N

```bash
[root@CommunityServer ~]# echo -e '1\n2'|sed 'n;p'
1
2
2
[root@CommunityServer ~]# echo -e '1\n2'|sed 'N;p'
1
2
1
2
```

* p vs P

```bash
[root@CommunityServer ~]# echo -e '1\n2'|sed 'N;p'
1
2
1
2
[root@CommunityServer ~]# echo -e '1\n2'|sed 'N;P'
1
1
2
```

* d vs D

```bash
[root@CommunityServer ~]# echo -e '1\n2'|sed 'N;d'
[root@CommunityServer ~]# echo -e '1\n2'|sed 'N;D'
2
```
