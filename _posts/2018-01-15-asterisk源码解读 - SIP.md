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

### 2. 整体数据流

```c
//为socket io添加监听事件（以UDP为例，TCP采用tcp_helper）
static void *do_monitor(void *data) {
    sipsock_read_id = ast_io_add(io, sipsock, sipsock_read, AST_IO_IN, NULL);
}

//所有UDP数据都经过sipsock_read回调
static int sipsock_read(int *id, int fd, short events, void *ignore) {
    //读取socket数据并放入req.data
    //读取socket地址并作为handle_request_do第二个参数传入
    handle_request_do(&req, &addr);
}

static int handle_request_do(struct sip_request *req, struct ast_sockaddr *addr) {
    //判断是否是debug ip, sip_debug_test_addr, 并置req->debug=1，后续将打印该ip的所有信令
    //解析内容判断合法性，并放入req->method、req->header、req->line (body)
    //查找或创建会话sip_pvt
    handle_incoming(p, req, addr, &recount, &nounlock)
}

static int handle_incoming(struct sip_pvt *p, struct sip_request *req, struct ast_sockaddr *addr, int *recount, int *nounlock) {
    //如果是客户端回复包（Trying、Ringing等）调用handle_response
    if (req->method == SIP_RESPONSE) {
        handle_response(p, respid, e + len, req, seqno);
        return 0
    } 
    //否则根据Method进行路由（handle_request_xxxxx）
    switch (p->method) {
    case SIP_INVITE:
        res = handle_request_invite(p, req, addr, seqno, recount, e, nounlock);
        break;
    case SIP_CANCEL:
        res = handle_request_cancel(p, req);
        break;
    case SIP_BYE:
        res = handle_request_bye(p, req);
        break;
    case SIP_MESSAGE:
        res = handle_request_message(p, req, addr, e);
        break;
    case SIP_REGISTER:
        res = handle_request_register(p, req, addr, e);
        break;
    }
}

```

### 3. 业务流

##### 3.1 读取MySQL数据库

当sip用户密码等信息存储于数据库，则通过如下调用栈进行数据读取和写入
```c
sip_find_peer_full -> realtime_peer -> realtime_peer_by_name -> ast_load_realtime -> ast_load_realtime_fields -> ast_load_realtime_all_fields -> mysql_engine.realtime_func (res_config_mysql.c) -> realtime_mysql
```

##### 3.2 呼叫流程

执行extension.conf配置规则（exten => _X.,1,Dial(SIP/${EXTEN}, 20))
```c
handle_request_invite -> ast_pbx_start -> __ast_pbx_run -> ast_spawn_extension -> pbx_extension_helper -> pbx_exec -> app.execute -> dial_exec (app_dial.c)  -> dial_exec_full
```

```c
dial_exec_full -> ast_request -> sip_tech.requester -> sip_request_call
...
dial_exec_full -> ast_call -> sip_tech.call -> sip_call
``` 