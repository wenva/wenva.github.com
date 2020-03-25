---
layout: post
title: "关于Github上的Contributions不记录问题"
date: 2015-07-03
comments: false
categories: 版本管理
---
很长时间一段时间都认为Github的Contributions只有通过pull request才能更新，今天特地Google了下，发现原来不是如此，关于Contributions，Github给出了答案。

以下情况Contributions将被记录:

### 1. issues and pull requests
* 一年内
* 自己的库（非fork）

### 2. Commits
* 一年内
* 邮箱地址一致
* Master分支下

### 3. Fork
* 需要Star
* pull request或issue
* 是组织的一员


于是我发现应该是邮箱不一致导致的，通过
<pre>
git config user.email
</pre>
发现邮箱与Github上的不一样（由于我还用了GitLab），通过如下修改
<pre>
git config --global user.email "xxxx@xxx.com"
</pre>

修改后尝试commit，发现ok. 终于可以好好玩耍Contributions了.
