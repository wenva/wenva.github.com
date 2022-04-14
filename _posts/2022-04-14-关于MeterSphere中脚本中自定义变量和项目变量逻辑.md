---
layout: post
title: "关于MeterSphere中脚本中自定义变量和项目变量逻辑"
date: 2022-04-14
comments: false
categories: 运维
---

近期在使用MeterSphere前置/后置脚本时候，对于项目变量有比较大的困惑：

```
（1）为什么需要同时调用2次put，`vars.put(${__metersphere_env_id}+"key","value");vars.put("key","value")`
（2）单独设置`vars.put(${__metersphere_env_id}+"key","value")`，为什么取不到值
（3）自定义变量和项目变量的声明周期是怎样
```

于是今天对其整个过程进行了猜想，并通过实际debug，得出了结论，现分享如下

##### 结论

整个流程如下：

*（1）系统调用脚本前，将数据库metersphere/api_test_environment表config自动中的variables及系统一个参数载入到vars变量中

```
{
    "key": "value"
}
```

*（2）若执行`vars.put("key","value1")`，则会覆盖vars中key的值

```
{
    "key": "value1"
}
```

* (3) 若执行`vars.put(${__metersphere_env_id}+"key","value2")`，则会在vars新增${__metersphere_env_id}+"key"

```
{
    "key": "value1"
    ${__metersphere_env_id}+key: "valu2"
}
```

这里就解释了文章开头提到的2个问题

* (4) 脚本结束后，系统会把${__metersphere_env_id}开头的key，去除${__metersphere_env_id}并存储到metersphere/api_test_environment的config字段，其他值则丢弃


##### 实际调试

```
//打印vars对象中所有键值
void printVars() {
    Iterator it = vars.getIterator();

    while (it.hasNext()) {
        Map.Entry v = it.next();
        log.info(v.getKey() + ": " + v.getValue());
    }
}

//步骤1

log.info("===>(1)初始化阶段：将保存的项目环境参数加载到vars对象中");

printVars();

//步骤2
log.info("===>(2)设置自定义变量，若已有则覆盖");

vars.put("key", "value1");

printVars();

//步骤3
log.info("===>(3)设置项目环境参数，会把__metersphere_env_id+key添加到vars");

vars.put(${__metersphere_env_id}+"key", "value2");

printVars();
```

输出：

```
2022-04-14 10:28:12 INFO ThreadGroup 1-1 ===>(1)初始化阶段：将保存的项目环境参数加载到vars对象中
...
2022-04-14 10:28:12 INFO ThreadGroup 1-1 key: value
...
2022-04-14 10:28:12 INFO ThreadGroup 1-1 ===>(2)设置自定义变量，若已有则覆盖
...
2022-04-14 10:28:12 INFO ThreadGroup 1-1 key: value1
...
2022-04-14 10:28:12 INFO ThreadGroup 1-1 ===>(3)设置项目环境参数，会把__metersphere_env_id+key添加到vars
...
2022-04-14 10:28:12 INFO ThreadGroup 1-1 MS.ENV.9c78be4a-6fdd-4fbc-b427-ac7ca585e73f.key: value2
...
2022-04-14 10:28:12 INFO ThreadGroup 1-1 key: value1
...
```

数据库中metersphere/api_test_environment表config字段

```
{
  ...
  "commonConfig": {
    "variables": [
      {
        "enable": true,
        "name": "key",
        "value": "value2"
      }
      ...
    ],
    "hosts": [],
    "enableHost": false,
    "requestTimeout": 60000,
    "responseTimeout": 60000
  }
  ...
}
```
