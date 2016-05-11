---
layout: post
title: "关于xargs与alias矛盾"
date: 2016-05-11
comments: false
categories: shell
---

xargs和alias是UNIX/类UNIX下比较常用的命令，而且也非常好用；他们非常和谐的各自活着，可是有一天，有一个攻城狮把他俩凑在一起，于是他们吵架了，闹矛盾了. 我们一起来看看为何吵架？

## xargs

<pre>
xargs [-0opt] [-E eofstr] [-I replstr [-R replacements]] [-J replstr] [-L number] [-n number [-x]] [-P maxprocs] [-s size] [utility [argument ...]]
</pre>

xargs从标准输入读取内容，并将这些内容作为参数传递给utility，utility可以是命令或可执行文件.

<pre>
echo 'hello'|xargs printf 
</pre>

## alias

<pre>
alias [-p] [name[=value] ... ]
</pre>

alias起到别名的作用，一般有两个作用，一个是缩短命令长度，二是起别名.

<pre>
alias ll='ls -al'
</pre>

## 矛盾
在正常使用过程中，也许大家并不会觉得有什么坑，但是当两个合在一起用，就会出现. 

<pre>
alias pr='printf'
echo 'hello'|xargs pr
</pre>
PS: 按正常思路，应该是输出`hello`，可惜报出如下错误`pr: cannot open hello, No such file or directory`

查了下资料发现:

> alias属于bash的内部命令，外部命令是无法识别的，而xargs则是外部命令，可以通过which查看

那么问题总要解决，该如何解决，总不会在/usr/local/bin下创建个pr文件，这么繁琐的事肯定不干，于是继续搜索，终于还是找到解决方案:

<pre>
alias [-p] [name[=value] ...]
...
A trailing space in  value causes the next word to be checked for alias substitution when the alias is expanded.
</pre>
PS: 大致含义是当value后面加上一个空格，则下一个单词也会用alias一起替换

<pre>
alias xargs='xargs ' #此处加一空格
alias pr='printf'
echo 'hello'|xargs pr
</pre>
