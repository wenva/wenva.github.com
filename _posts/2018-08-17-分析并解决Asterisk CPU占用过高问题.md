---
layout: post
title: "分析并解决Asterisk CPU占用过高问题"
date: 2018-08-17
comments: false
categories: SIP
---

现象：近来，发现Asterisk SIP服务经常占用CPU 100%以上，而且都在服务启动1个小时后出现，但重启服务后就恢复正常

初步分析：通过tshark对网络发包测试，并未发现有明显变化，因此不是请求量变大引发的CPU紧张（从重启服务恢复正常也可以证实），因此可以确定是服务内部的问题，得益于 [《Why does Asterisk consume 100% CPU?》](https://moythreads.com/wordpress/2009/05/06/why-does-asterisk-consume-100-cpu/) 这篇文章，我对asterisk服务进行了深度剖析，过程如下


### 步骤1. 获取哪个线程（Light Weight Process）占用CPU最高

ps -LlFm -p `pidof asterisk`

```
F S UID        PID  PPID   LWP  C NLWP PRI  NI ADDR SZ WCHAN    RSS PSR STIME TTY          TIME CMD
4 - root     13090 13088     - 25   47   -   - - 522547 -     573636  - 08:43 pts/18   00:07:28 /usr/sbin/asterisk -f -vvvg -c
4 S root         -     - 13090  0    -  80   0 -     - poll_s     -   1 08:43 -        00:00:00 -
1 S root         -     - 13091  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13092  0    -  80   0 -     - futex_     -   0 08:43 -        00:00:17 -
1 R root         -     - 13093  3    -  80   0 -     - -          -   0 08:43 -        00:01:01 -
1 S root         -     - 13094  1    -  80   0 -     - futex_     -   1 08:43 -        00:00:19 -
1 S root         -     - 13096  0    -  80   0 -     - poll_s     -   0 08:43 -        00:00:00 -
1 S root         -     - 13098  0    -  80   0 -     - futex_     -   0 08:43 -        00:00:02 -
1 S root         -     - 13100  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13101  0    -  80   0 -     - futex_     -   0 08:43 -        00:00:00 -
1 S root         -     - 13102  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13103  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13104  2    -  80   0 -     - futex_     -   1 08:43 -        00:00:48 -
1 S root         -     - 13105  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13106  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13107  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13108  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13109  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13110  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13111  0    -  80   0 -     - futex_     -   0 08:43 -        00:00:00 -
1 S root         -     - 13112  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13113  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13114  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13115  0    -  80   0 -     - inet_c     -   1 08:43 -        00:00:00 -
1 S root         -     - 13116  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13117  0    -  80   0 -     - poll_s     -   0 08:43 -        00:00:00 -
1 S root         -     - 13118  0    -  80   0 -     - futex_     -   0 08:43 -        00:00:00 -
1 S root         -     - 13119  0    -  80   0 -     - poll_s     -   0 08:43 -        00:00:00 -
1 R root         -     - 13120 16    -  80   0 -     - -          -   0 08:43 -        00:04:52 -
1 S root         -     - 13121  0    -  80   0 -     - futex_     -   1 08:43 -        00:00:00 -
1 S root         -     - 13122  0    -  80   0 -     - futex_     -   0 08:43 -        00:00:00 -
1 S root         -     - 13123  0    -  80   0 -     - poll_s     -   1 08:43 -        00:00:00 -
1 S root         -     - 13124  0    -  80   0 -     - hrtime     -   0 08:43 -        00:00:00 -
1 S root         -     - 13125  0    -  80   0 -     - futex_     -   0 08:43 -        00:00:00 -
1 S root         -     - 13126  0    -  80   0 -     - poll_s     -   0 08:43 -        00:00:00 -
1 S root         -     - 13127  0    -  80   0 -     - futex_     -   0 08:43 -        00:00:00 -
1 S root         -     - 13128  0    -  80   0 -     - poll_s     -   1 08:43 -        00:00:00 -
1 S root         -     - 13129  0    -  80   0 -     - hrtime     -   1 08:43 -        00:00:00 -
1 S root         -     - 13130  0    -  80   0 -     - hrtime     -   0 08:43 -        00:00:00 -
1 S root         -     - 13131  0    -  80   0 -     - poll_s     -   0 08:43 -        00:00:00 -
```

其中C列表示线程占用CPU的百分比（这个值是自服务启动到目前的平均值，而top命令是实时，因此与top会不一致），从以上我们可以确定是13120线程占用最高，接下来我们要分析13120到底执行了什么

### 步骤2. 获取具体线程执行堆栈信息

pstack `pidof asterisk`
```
Thread 21 (Thread 0x7fecd94ea700 (LWP 13120)):
#0  0x00000000005aee3f in tps_cmp_cb ()
#1  0x00000000004580a5 in internal_ao2_traverse ()
#2  0x0000000000458b51 in __ao2_find ()
#3  0x00000000005aef0d in ast_taskprocessor_create_with_listener ()
#4  0x00000000005b4f1e in ast_threadpool_serializer ()
#5  0x000000000059acc1 in internal_stasis_subscribe.clone.1 ()
#6  0x00000000005a6168 in stasis_message_router_create_internal ()
#7  0x00000000004ef227 in endpoint_internal_create ()
#8  0x00007fecf0ec76c6 in build_peer () from /usr/lib/asterisk/modules/chan_sip.so
#9  0x00007fecf0ed5a48 in realtime_peer () from /usr/lib/asterisk/modules/chan_sip.so
#10 0x00007fecf0ed6646 in sip_find_peer_full () from /usr/lib/asterisk/modules/chan_sip.so
#11 0x00007fecf0ed66b7 in sip_find_peer () from /usr/lib/asterisk/modules/chan_sip.so
#12 0x00007fecf0f00aa7 in register_verify () from /usr/lib/asterisk/modules/chan_sip.so
#13 0x00007fecf0f02cb5 in handle_request_register () from /usr/lib/asterisk/modules/chan_sip.so
#14 0x00007fecf0f0d166 in handle_incoming () from /usr/lib/asterisk/modules/chan_sip.so
#15 0x00007fecf0f0ed84 in handle_request_do () from /usr/lib/asterisk/modules/chan_sip.so
#16 0x00007fecf0f10786 in sipsock_read () from /usr/lib/asterisk/modules/chan_sip.so
#17 0x0000000000514b52 in ast_io_wait ()
#18 0x00007fecf0ed4c6b in do_monitor () from /usr/lib/asterisk/modules/chan_sip.so
```

从以上我们可以发现与创建taskprocessors有关，于是我们看下了taskprocessors数量

asterisk -rx 'core show taskprocessors'

```
5d07f1f8-56be-4456-ac64-08dd619b09a9                   2            0            1
88498730-b675-433d-b71c-eaa51fde68b6                   2            0            1
eaabf337-81d5-4411-a0dc-a05f20071c7c                   2            0            1
9dc17b55-f7cb-4ff4-bbcd-44033893eb4f                   2            0            1
afa4cfff-4cb9-451b-a5d1-7ace2e4a9040                   2            0            0
67729e31-8e78-423b-b5d5-dd746190f374                   2            0            0
b9b5e393-f016-4d09-b8fe-03d7633ef174                   2            0            0
    +---------------------+-----------------+------------+-------------+
    55585 taskprocessors
```

通过以上推测，应该是大量的taskprocessors占用的CPU资源，而且taskprocessors会不停增加

### 步骤3：结合代码，确认原因

```c
struct ast_taskprocessor *ast_taskprocessor_create_with_listener(const char *name, struct ast_taskprocessor_listener *listener)
{
    struct ast_taskprocessor *p = ao2_find(tps_singletons, name, OBJ_KEY);

    if (p) {
        ast_taskprocessor_unreference(p);
        return NULL;
    }
    return __allocate_taskprocessor(name, listener);
}
```
ao2_find是根据name从任务队列中查找，一旦这个队列非常大，那CPU需要不停比较，从而会占用大量CPU资源，至此，问题基本确定了；接下来就要进入苦活阶段

### 步骤4：解决代码BUG
通过分析代码发现如下关系： peer->endpoint->route->subscription->mailbox

mailbox就是"struct ast_taskprocessor"即任务对象，因此可以推断应该是这个依赖链中有对象内存泄露了导致mailbox没有从任务队列中移除，通过一级一级分析，发现是peer内存泄露了，看如下代码

```c
    } else if (!strcasecmp(curi, "*") || !expire) { /* Unregister this peer */
        /* This means remove all registrations and return OK */
        struct sip_peer* peer_db = sip_find_peer_by_db(peer->peername, NULL, TRUE, FINDPEERS, FALSE, 0);
        //ast_log(LOG_WARNING, "unregister found name%s\n",peer->peername);
        if(peer_db!=NULL && peer->uuid!=NULL && peer_db->uuid!=NULL)
        {
            //ast_log(LOG_WARNING, "db_uuid%s,peer_uuid%s\n", peer_db->uuid,peer->uuid);
            if(strcmp(peer->uuid,peer_db->uuid) == 0)
            {
                AST_SCHED_DEL_UNREF(sched, peer->expire,
                    sip_unref_peer(peer, "remove register expire ref"));
                ast_verb(3, "Unregistered SIP '%s'\n", peer->name);
                expire_register(sip_ref_peer(peer,"add ref for explicit expire_register"));
                return PARSE_REGISTER_UPDATE;
            }
            else
            {
                ast_log(LOG_WARNING, "Invalid unregister db_uuid%s,but peer_uuid%s\n", peer_db->uuid,peer->uuid);
            }
        }
```
peer_db是sip_find_peer_by_db得到的，而sip_find_peer_by_db是有'加引用'的，因此在没用peer_db时需要执行'去引用'，因此此处需要加sip_unref_peer(peer_db, "remove")

当然代码中还有其他地方也是类似，这里不一一列出，改完所有泄露，重新编译运行发现taskprocessors不会不断增加，维持在30个以内，通过几个小时的运行，CPU没有增高，此问题得到的最终解决。

### 总结

【授之以鱼，不如授之以渔】以上只是一种CPU过高的原因，各位很可能遇到的问题不一样，但都可以借鉴上面步骤对问题进行排查。
