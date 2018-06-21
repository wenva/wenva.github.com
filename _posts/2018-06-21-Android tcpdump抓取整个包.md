---
layout: post
title: "Android tcpdump抓取整个包"
date: 2018-06-21
comments: false
categories: 技巧
---

```bash
tcpdump -s 0 
```
`-s 0`表示抓取整个包，否则只会抓取头部