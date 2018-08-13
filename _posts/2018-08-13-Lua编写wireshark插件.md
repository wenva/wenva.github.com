---
layout: post
title: "Lua编写wireshark插件"
date: 2018-08-13
comments: false
categories: 技巧
---

在我们自己的系统中，会自定义协议，甚至加密；为了更容易进行抓包分析，我们需要编写wireshark插件.

### 前提

wireshark需要支持Lua，可以打开Wireshark，进入关于界面，若带有"with Lua x.x.x"，则表示支持，否则请升级; 命令行方式可以使用`tshark -v`查看，我的版本信息如下

```bash
TShark (Wireshark) 2.2.3 (v2.2.3-0-g57531cd)

Copyright 1998-2016 Gerald Combs <gerald@wireshark.org> and contributors.
License GPLv2+: GNU GPL version 2 or later <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Compiled (64-bit) with libpcap, without POSIX capabilities, with GLib 2.36.0,
with zlib 1.2.5, with SMI 0.4.8, with c-ares 1.12.0, with lua 5.2.4, with GnuTLS
2.12.19, with Gcrypt 1.5.0, with MIT Kerberos, with GeoIP.

Running on Mac OS X 10.12.6, build 16G29 (Darwin 16.7.0), with locale
C/UTF-8/C/C/C/C, with libpcap version 1.8.1 -- Apple version 67.60.1, with
GnuTLS 2.12.19, with Gcrypt 1.5.0, with zlib 1.2.8.
Intel(R) Core(TM) i5-4258U CPU @ 2.40GHz (with SSE4.2)

Built using llvm-gcc 4.2.1 (Based on Apple Inc. build 5658) (LLVM build
2336.9.00).
```

### 配置

* 界面

打开wireshark安装目录的init.lua文件，在最后添加"dofile(...)"

vim /Applications/Wireshark.app/Contents/Resources/share/wireshark/init.lua
```bash
DATA_DIR = Dir.global_config_path()
USER_DIR = Dir.personal_config_path()

dofile(DATA_DIR.."console.lua")
dofile(USER_DIR.."xxxxx.lua")
```
PS: DATA_DIR表示全局配置路径，USER_DIR表示用户配置路径，可以通过【"关于Wireshark" -> "文件夹"】查看全局配置和用户路径

* 命令行

```bash
tshark -X lua_script:xxx.lua 
```
PS: xxx.lua可以带路径，但不能用~

### 编写lua

如下是模板代码，可以在此基础上进行扩展

```lua
-- 获取对应解析表，DissectorTable.get(tablename)
-- 可以通过"Decode As..."查看所有表名，本例是添加udp 4444端口的解析
local udp_table = DissectorTable.get("udp.port")

-- 创建协议，Proto.new(name, desc), name不能有空格
local my_proto = Proto("myproto", "my proto description")

-- 定义字段内容 ProtoField.new(name, abbr, base), base表示以什么方式展现，有base.DEC, base.HEX, base.OCT, base.DEC_HEX, base.DEC_HEX or base.HEX_DEC
local magicField = ProtoField.uint16("Magic", "Magic", base.HEX)
my_proto.fields = {magicField}

--协议解析，buffer是数据部分，pinfo是wireshark列表信息，有Protocol, Info等
function my_proto.dissector(buffer, pinfo, tree)

    -- 在列表的Protocol栏目中展现
    pinfo.cols.protocol:set("MYPROTO")
    local len = buffer:len()

    -- 在列表的Info栏目中展现
    pinfo.cols.info = 'HELLO MY PROTO'

    -- 添加自定义协议根节点
    local myProtoTree = tree:add(my_proto, buffer(0, len), "MYPROTO Protocol")
    local offset = 0

    -- 添加字段
    myProtoTree:add(magicField, buffer(offset, 2))
end

--增加协议
udp_table:add(4444, my_proto)
```

### 测试

```bash
smou:~ $ tshark -i en0 -X lua_script:test.lua port 4444
  1   0.000000 192.168.113.75 → 120.24.89.194 MYPROTO 47 HELLO MY PROTO
```
PS: 可以添加-V展现树节点