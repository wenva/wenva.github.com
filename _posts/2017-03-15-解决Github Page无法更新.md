---
layout: post
title: "解决Github Page无法更新"
date: 2017-03-15
comments: false
categories: Github
---

春节后，写了一篇文章提交到Github，发现pages没有更新，原先以为Github问题，等了2天，发现一直不更新，于是去查了下什么原因，原来Github在构建pages失败时，会发送邮件给你的邮箱（由于设置了另外一个邮件，因此一直没察觉），查看邮件（也可以进入repo设置界面查看），发现真的是构建失败，给出的提示是`Your site is having problems building: Page build failed. For more information, see https://help.github.com/articles/troubleshooting-github-pages-builds/.`于是点击相应连接，了解到`Page build failed`是构建失败，具体原因可以尝试在本地构建。Github给出了[本地构建方法](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/#platform-linux)

这里总结构建过程下：

##### 1. 安装bunder
```
gem install bunder
```

##### 2. [安装jekyll](http://jekyllrb.com/)
```
gem install jekyll bundler
```

##### 3. 在工程主目录生成Gemfile，内容如下
```
source 'https://rubygems.org'
gem 'github-pages', group: :jekyll_plugins
```
##### 4. 构建

```
bundle exec jekyll serve
```

构建完后报出了如下错误：

```
  Conversion error: Jekyll::Converters::Markdown encountered an error while converting '_posts/2015-06-05-Ruby学习路程.md':
                    Can't handle generic non-integer character reference 'laquo_space'
jekyll 3.4.1 | Error:  Can't handle generic non-integer character reference 'laquo_space'
```
提示还是比较明显的，是原来的一篇文章语法错误，原来是标题使用了\<\<

```
### 5. \<\< self 理解
```

于是添加转义符修正，并提交更新到Github，发现更新正常了。
