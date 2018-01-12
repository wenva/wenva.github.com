---
layout: post
title: "asterisk中fullcontact私有IP导致被呼叫失败"
date: 2018-01-08
comments: false
categories: SIP
---

最近发现某些注册到asterisk的SIP客户端无法被呼叫，抓包确定是由于asterisk往私有IP发送数据，通过对比发现这些客户端发送的SIP信息Contact字段是私有IP，google了下相关资料并未找到解决方法，于是跟踪了下代码，找出了原因，现梳理如下：

以下给出被呼叫调用栈（chan_sip.c），代码是基于13.2.1，不同版本会有些差异

* 
* CSeq 序列号，用于标识请求，服务器会原样返回，且需要呈现递增状态


* sipsock_read（UDP，TCP使用_sip_tcp_helper_thread）
    * 读取socket数据并放入req.data
    * 读取socket地址并作为handle_request_do第二个参数传入
* handle_request_do
    * 判断是否是debug ip, sip_debug_test_addr, 并置req->debug=1，后续将打印该ip的所有信令
    * 解析内容判断合法性，并放入req->method、req->header、req->line (body)
    * 查找或创建会话sip_pvt
* handle_incoming
    * 如果是客户端回复包（Trying、Ringing等）调用handle_response
    * 根据Method进行路由（handle_request_xxxxx）





#### 读取数据库

* sip_find_peer_full -> realtime_peer -> realtime_peer_by_name -> ast_load_realtime -> ast_load_realtime_fields -> ast_load_realtime_all_fields -> mysql_engine.realtime_func (res_config_mysql.c) -> realtime_mysql

```c




static enum check_auth_result check_user_full(struct sip_pvt *p, struct sip_request *req,
                          int sipmethod, const char *uri, enum xmittype reliable,
                          struct ast_sockaddr *addr, struct sip_peer **authpeer)
{
    res = check_peer_ok(p, name, req, sipmethod, addr,
            authpeer, reliable, calleridname, uri2);
}

static enum check_auth_result check_peer_ok(struct sip_pvt *p, char *of,
    struct sip_request *req, int sipmethod, struct ast_sockaddr *addr,
    struct sip_peer **authpeer,
    enum xmittype reliable, char *calleridname, char *uri2)
{
    if (sipmethod == SIP_SUBSCRIBE) {
        peer = sip_find_peer(of, NULL, TRUE, FINDALLDEVICES, FALSE, 0);
    }
}


struct sip_peer *sip_find_peer(const char *peer, struct ast_sockaddr *addr, int realtime, int which_objects, int devstate_only, int transport)
{
    return sip_find_peer_full(peer, addr, NULL, realtime, which_objects, devstate_only, transport);
}


static struct sip_peer *sip_find_peer_full(const char *peer, struct ast_sockaddr *addr, char *callbackexten, int realtime, int which_objects, int devstate_only, int transport)
{
    ...
    if (!p && (realtime || devstate_only)) {
        p = realtime_peer(peer, addr, callbackexten, devstate_only, which_objects);
        ...
    }
    ...
}



static struct sip_peer *realtime_peer(const char *newpeername, struct ast_sockaddr *addr, char *callbackexten, int devstate_only, int which_objects)
{
    ...
    /* Peer found in realtime, now build it in memory */
    peer = build_peer(newpeername, var, varregs, TRUE, devstate_only);
    ...
}

static struct sip_peer *build_peer(const char *name, struct ast_variable *v, struct ast_variable *alt, int realtime, int devstate_only) {
    ...
    if (ast_str_strlen(fullcontact)) {
        ast_string_field_set(peer, fullcontact, ast_str_buffer(fullcontact));
        peer->rt_fromcontact = TRUE;
        if ((!ast_test_flag(&peer->flags[2],  SIP_PAGE3_NAT_AUTO_RPORT) && !ast_test_flag(&peer->flags[0], SIP_NAT_FORCE_RPORT))
            || ast_sockaddr_isnull(&peer->addr)) {
            __set_address_from_contact(ast_str_buffer(fullcontact), &peer->addr, 0);
        }
    }
    ...
}
```