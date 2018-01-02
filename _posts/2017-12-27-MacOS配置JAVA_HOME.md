---
layout: post
title: "MacOS配置JAVA_HOME"
date: 2017-12-27
comments: false
categories: 运维
---

```bash
export JAVA_HOME=$(/usr/libexec/java_home)
export PATH=$JAVA_HOME/bin:$PATH
export CLASS_PATH=$JAVA_HOME/lib
```