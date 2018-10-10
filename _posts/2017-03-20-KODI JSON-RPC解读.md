---
layout: post
title: "KODI JSON-RPC解读"
date: 2017-03-20
comments: false
categories: 树莓派
---

大概一年前就开始关注KODI了，确实是个非常不错的开源项目，KODI提供很好的操作界面，但作为一个命令行控或者是没有显示屏的树莓派，我希望能够通过命令行对其进行控制，比如播放、暂停、静音等等. 于是去搜索了下，发现有个JSON-RPC，他是kODI官网推出的，方便其他开发者对接，到目前为止已经更新到v8，可以点击[这里查看](http://kodi.wiki/view/JSON-RPC_API)。这里将为大家详细介绍下它的用法。

### 初步印象

在使用JSON-RPC，必须开启，可以进入设置 - 服务 - 控制，开启服务，可设置端口、用户名、密码，当然可以不设置用户名和密码

### 入门

JSON-RPC顾名思义就是采用JSON进行RPC通信，那么它的[基本格式](http://www.jsonrpc.org/specification)如下：

##### 请求(REQUEST)

* URI：http://host:port/jsonrpc
* METHOD：POST
* HEADER：ContentType:application/json
* BODY: {"jsonrpc":"2.0", "method":"xx", "params":{}, "id":xx},jsonrpc必须是2.0，这个与实际版本无关 method为具体方法，会在后面介绍，params为method对应的参数，若无，则可以不传 id是由客户端定义，用于标识客户端，服务器会返回相同的id（见响应）

如：

```
curl -X POST -H "ContentType:application/json" -d '{"jsonrpc": "2.0", "method": "JSONRPC.Version", "id":"22"}' http://localhost:8080/jsonrpc
```

##### 响应(RESPONSE)

* BODY:  {"jsonrpc":"2.0", "result":"xxx","error":{"code":xx,"message":"xxx","data":"xxx"},"id":xx }  result为返回结果，若错误，则空，error错误，id为请求传递的，若错误，为空


```
{"id":"22","jsonrpc":"2.0","result":{"version":{"major":8,"minor":0,"patch":0}}}
```

### 进阶

以上内容就好比是内功，有了好的内功，其他的都好学，在之前的REQUEST我们了解到了method和params，那么我们来看看都有哪些外功. 外功分为v2、v4、v6、v8几个版本，目前最新的是v8，可以通过上面给出的例子，获取到当前版本. 竟然我用到的是v8，我们就来看下[v8](http://kodi.wiki/view/JSON-RPC_API/v8)的定义。 v8是随着kodi v17一同发布的，它支持WebSocket。正所谓举其一可知大概，我在这里就不对所有的method进行介绍，我会抽出几个，告知大家如何看懂文档。

* Player.GetActivePlayers - 获取当前激活的播放器


```
5.9.1 Player.GetActivePlayers
Returns all active players
Permissions:
    ReadData
Returns:
    Type: array
```
Permissions 权限，可通过JSONRPC.Permission获取权限开关状态
Returns：返回


```
curl -X POST --header "content-type:application/json" --data '{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id":"22"}' http://localhost:8080/jsonrpc

{"id":"22","jsonrpc":"2.0","result":[{"playerid":0,"type":"audio"}]}
```


* Application.SetVolume - 设置音量


```
5.2.4 Application.SetVolume
Set the current volume
Permissions:
    ControlPlayback
Parameters:
    mixed volume
Returns:
    Type: integer
```

例子：


```
 curl -X POST --header "content-type:application/json" --data '{"jsonrpc": "2.0", "method": "Application.SetVolume", "params":{"volume":8}, "id":"22"}' http://localhost:8080/jsonrpc
 
{"id":"22","jsonrpc":"2.0","result":8}
```

### 扩展

当然KODI还提供了kodi-send命令，来简化请求，格式如下：


```
 kodi-send -a "XXX"
```

xxx见http://kodi.wiki/view/List_of_built-in_functions

如


```
osmc@osmc:~$ kodi-send -a "SetVolume(10)"
Sending action: SetVolume(10)
```



