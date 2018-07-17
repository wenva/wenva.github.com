---
layout: post
title: "sed的hold space"
date: 2018-07-17
comments: false
categories: 技巧
---

hold space - 是sed上一次pattern space的缓存

* sed 工作流程

```bash
1. 读入一行
2. 放入pattern space
3. 执行命令
4. 打印pattern space
5. 拷贝pattern space至hold space
6. 清空pattern space
```

* 相关命令

```bash

h - 使用pattern space替换hold space
H - hold space添加一行，并将pattern space内容追加至hold space
g - 使用hold space替换pattern space
G - pattern space添加一行，并将hold space内容追加至pattern space
x - 交换pattern space与hold space内容
```