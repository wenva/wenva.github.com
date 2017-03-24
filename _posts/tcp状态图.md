# TCP状态图

在使用netstat发现有个State字段，于是脑补了下，发现水还是蛮深的，以前只了解三次握手、四次握手，并没有了解其中的状态，大家可以直接搜索`TCP状态图`，如下：

![image](http://www.cnitblog.com/images/cnitblog_com/wildon/544465b00200001s.png)

我这里将对其进行整理，方便大家理解，看图前，先看下术语描述：

* S - 表示发送
* R - 表示接收

## 连接建立阶段（三次握手）

```
CLOSE                                  ESTABLISH
  |                                        |
  |---------------- CLIENT ----------------|
  |                                        |
  |           SYN_SEND                     |
  |              |                         |
  |              |       R: SYN ACK        |
  |------------->|------------------------>|
  |    S: SYN    |          S: ACK         |
  |              |                         |
  |                                        |
  |                                        |
  |                                        |
  |---------------- SERVER ----------------|
  |                                        |
  |           LISTEN        SYN_RECV       |
  |              |              |          |
  |     OPEN     |    R: SYN    |  R: ACK  |
  |------------->|------------->|--------->|
  |              |  S: SYN ACK  |          |
  |              |              |          |
  |              |              |          |
  |              |<-------------|          |
  |              |              |          |

```

* CLOSE - 关闭态
* LISTEN - 监听态（被动打开）
* SYN_SEND - SYN发送态（已发送SYN）
* SYN_RECV - SYN接收态（已接收SYN，并发送ACK）
* ESTABLISH - 连接态
* 三次握手: 客户端发送SYN -> 服务端接收SYN，并发送SYN、ACK -->  客户端接收SYN、ACK，并发送ACK
* **RST: SYN_RECV发送RST可以回到LISTEN，主要用于处理异常连接**

## 连接结束阶段（四次握手）
