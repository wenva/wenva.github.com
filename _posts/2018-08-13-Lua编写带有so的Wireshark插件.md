---
layout: post
title: "Lua编写带有so的Wireshark插件"
date: 2018-08-13
comments: false
categories: 技巧
---

wireshark支持纯lua和c插件，那么如何支持lua和c混编的问题，即lua调用c接口，对于lua语言，这个不是问题，但加上环境，就会出现如下问题

## 问题1. 如何编译正确的so

直接通过以下语句，就可以生成so
```bash
gcc test.c -fPIC -shared -o test.so -llua
```
通过以上语句确实可以生成so，但链接的是系统lua库，一旦系统lua与wireshark自带lua版本不一致，就可以导致实际无法运行

这里讲个实际的例子，我系统lua是5.3.4是支持luaL_newlib，但wireshark却是5.2.3，没有luaL_newlib，因此会报找不到对应symbol，而需要改为luaL_openlib

```c
extern int luaopen_test(lua_State* L)
{
    luaL_openlib(L, "test", mytest, 0);
    return 1;
}
```

因此正确做法，需要链接wireshark对应的动态库

```bash
gcc test.c -fPIC -shared -o test.so -L/Applications/Wireshark.app/Contents/Frameworks -lwireshark.8.1.3
```

### 问题2. 如何让wireshark加载so

lua中添加

```lua
test=require 'test'
```

打开Wireshark，会给出如下提示

```
Lua: Error during loading:
 /Users/smou/.config/wireshark/test.lua:6: module 'test' not found:
    no field package.preload['test']
    no file '/usr/local/share/lua/5.2/test.lua'
    no file '/usr/local/share/lua/5.2/test/init.lua'
    no file '/usr/local/lib/lua/5.2/test.lua'
    no file '/usr/local/lib/lua/5.2/test/init.lua'
    no file './test.lua'
    no file '/usr/local/lib/lua/5.2/test.so'
    no file '/usr/local/lib/lua/5.2/loadall.so'
    no file './test.so'
```
PS: 我们只要将so拷贝到/usr/local/lib/lua/5.2/中即可
