---
layout: post
title: "Lua编写wireshark插件"
date: 2018-08-13
comments: false
categories: 技巧
---

在我们自己的系统中，会自定义协议，甚至加密；为了更容易进行抓包分析，我们需要编写wireshark插件，以便更好展现.

### 前提

wireshark需要支持Lua，可以打开Wireshark，进入关于界面，若带有"with Lua x.x.x"，则表示支持，否则请升级; 命令行方式 `tshark -v`

### 配置

* 界面
打开wireshark安装目录的init.lua文件，在最后，添加"dofile"

vim /Applications/Wireshark.app/Contents/Resources/share/wireshark/init.lua
```bash
DATA_DIR = Dir.global_config_path()
USER_DIR = Dir.personal_config_path()

dofile(DATA_DIR.."console.lua")
dofile(USER_DIR.."h264_export.lua")
```
PS: DATA_DIR表示全局配置路径，USER_DIR表示用户配置路径，可以通过【"关于Wireshark" -> "文件夹"】查看全局配置和用户路径

* 命令行

```bash
tshark -X lua_script:xxx.lua 
```
PS: 必需是全路径，或者当前路径，不能用~等

### 编写lua

```lua
-- 获取对应解析表，DissectorTable.get(tablename)
-- 可以通过"Decode As...",查看所有表名，本例是添加udp 4444端口的解析
local udp_table = DissectorTable.get("udp.port")

-- 创建协议，Proto.new(name, desc), name不能有空格
local my_proto = Proto("myproto", "my proto description")

-- 定义字段内容 ProtoField.new(name, abbr, base), base表示以什么方式展现，有base.DEC, base.HEX, base.OCT, base.DEC_HEX, base.DEC_HEX or base.HEX_DEC
local magicField = ProtoField.uint16("Magic", "Magic", base.HEX)
my_proto.fields = {magicField}

--协议解析，buffer是数据部分，pinfo是wireshark列表信息（未展开状态），有Protocol, Info等
function my_proto.dissector(buffer, pinfo, tree)

    -- 在列表的Protocol中展现
    pinfo.cols.protocol:set("MYPROTO")
    local len = buffer:len()

    -- 在列表的Info中展现
    pinfo.cols.info = 'HELLO MY PROTO'

    -- 在展开项中展现
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
smou:~ $ tshark -V -i en0 -X lua_script:test.lua port 4444
Capturing on 'Wi-Fi'
Frame 1: 46 bytes on wire (368 bits), 46 bytes captured (368 bits) on 

...

User Datagram Protocol, Src Port: 65494, Dst Port: 4444
    Source Port: 65494
    Destination Port: 4444
    Length: 12
    Checksum: 0x8899 [unverified]
    [Checksum Status: Unverified]
    [Stream index: 0]
MYPROTO Protocol
    Magic: 0x3131
```