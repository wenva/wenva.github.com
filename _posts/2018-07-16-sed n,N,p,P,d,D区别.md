---
layout: post
title: "sed n,N,p,P,d,D区别"
date: 2018-07-16
comments: false
categories: SHELL
---

```
n - 打印当前行，读入下一行，且替换模式空间内容，即后续命令只对第二行生效；若遇到没有第二行的情况，则直接退出
N - 读入第二行，把两行都放入模式空间，并打印；若遇到没有第二行的情况，则直接退出
p - 打印模式空间内所有行
P - 只打印第一行
d - 删除模式空间内所有行
D - 只删除第一行
```

示例

* n vs N

```bash
[root@CommunityServer ~]# echo -e '1\n2'|sed 'n;p' （读入1，放入模式空间，执行n，打印1，将2替换入模式空间，执行p，打印2）
1
2
2
[root@CommunityServer ~]# echo -e '1\n2'|sed 'N;p'
1
2
1
2
smou:~ $ echo -e '1'|sed 'n' （先打印当前行，再读入第二行，发现没有第二行，则退出）
1
smou:~ $ echo -e '1'|sed 'N' （读入第二行，发现没有第二行，则退出）
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
