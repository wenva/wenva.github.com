---
layout: post
title: "asterisk源码解读 - SIP"
date: 2018-01-15
comments: false
categories: SIP
---

这几天阅读了下asterisk sip部分的源码（基于13.3.2版本），现梳理如下（代码只列出关键点）:

### 1. 模块装(卸)载

asterisk是采用模块方式来实现动态装卸载

```c
//定义ast_channel_tech变量，并赋值相应接口行为
struct ast_channel_tech sip_tech {
    .requster = sip_request_call,   //初始化会话
    .call = sip_call,               //呼叫
    .hangup = sip_hangup,           //挂掉
    .answer = sip_answer,           //接听
}

//定义加载函数
static int load_module(void) {
    ast_channel_register(&sip_tech);
}

//定义卸载函数
static int unload_module(void) {
    ast_channel_unregister(&sip_tech);
}

//注册模块
AST_MODULE_INFO(ASTERISK_GPL_KEY, AST_MODFLAG_LOAD_ORDER, "Session Initiation Protocol (SIP)",
        .support_level = AST_MODULE_SUPPORT_CORE,
        .load = load_module,
        .unload = unload_module,
        .reload = reload,
        .load_pri = AST_MODPRI_CHANNEL_DRIVER,
        .nonoptreq = "res_crypto,res_http_websocket",
```

### 2. 数据流

```c
//为socket io添加监听事件（以UDP为例，TCP采用tcp_helper）


```
