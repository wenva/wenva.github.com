---
layout: post
title: "gitlab之repos位置迁移"
date: 2016-06-06
comments: false
categories: 版本管理
---

前段时间gitlab服务出现503错误，查看了下日志，发现是gitlab数据所在的挂载点空间已经满了无法写入，于是想把数据迁移到另一个挂载点上，查了下gitlab仓库数据是位于`/var/opt/gitlab/git-data`下，于是最直接的做法就是把git-data拷贝到新挂载点下，然后建立一个软连接到`/var/opt/gitlab`下，而实际测试发现会有问题. 后来通过查看gitlab.rb配置文件，发现git_data_dir选项，于是通过把git_data_dir指向新挂载点，发现还是有问题，后来通过[stackoverflow](http://stackoverflow.com/questions/19902417/change-the-data-directory-gitlab-to-store-repos-elsewhere)找到了正确的方法，现记录于此:

### 1. 停止服务
<pre>
gitlab-ctl stop
</pre>

### 2. 修改git_data_dir
vim /etc/gitlab/gitlab.rb
<pre>
git_data_dir "/mnt/new/git-data"
</pre>

### 3. 拷贝
<pre>
rsync -av /var/opt/gitlab/git-data /mnt/new/git-data
</pre>
PS: 此处不能用cp，具体什么原因没有细查，有兴趣的童鞋可以去查查cp和rsync的区别

### 4. 生效配置
<pre>
gitlab-ctl reconfigure
</pre>

### 5. 启动服务
<pre>
gitlab-ctl start
</pre>
