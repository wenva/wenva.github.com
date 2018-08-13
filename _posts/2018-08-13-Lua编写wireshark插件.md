---
layout: post
title: "Lua编写wireshark插件"
date: 2018-08-13
comments: false
categories: 技巧
---

在我们自己的系统中，会自定义协议，甚至加密；为了更容易进行抓包分析，我们需要编写wireshark插件，以便更好展现.

### 前提

wireshark需要支持Lua，可以打开Wireshark，进入关于界面，若带有"with Lua x.x.x"，则表示支持，否则请升级;

### 配置

打开wireshark安装目录的init.lua文件，在最后，添加"dofile"

/Applications/Wireshark.app/Contents/Resources/share/wireshark/init.lua
```bash
DATA_DIR = Dir.global_config_path()
USER_DIR = Dir.personal_config_path()

dofile(DATA_DIR.."console.lua")
dofile(USER_DIR.."h264_export.lua")
```
PS: DATA_DIR表示全局配置路径，USER_DIR表示用户配置路径，可以通过【"关于Wireshark" -> "文件夹"】查看全局配置和用户路径

### 编写lua

模板
```lua
local udp_table = DissectorTable.get("udp.port")
local my_proto = Proto("DVP", "DVP Protocol", "DVP Protocol")

--定义协议字段内容
local magicField = ProtoField.uint16("Magic", "Magic", base.HEX)
my_proto.fields = {magicField}

--协议分析器
function my_proto.dissector(buffer, pinfo, tree)
    pinfo.cols.protocol:set("DVP")
    local len = buffer:len()
    local myProtoTree = tree:add(my_proto, buffer(0, len), "DVP Protocol")
    local offset = 0
    myProtoTree:add(magicField, buffer(offset, 2))

    -- 直接显示到未展开的info栏目，方便阅读
    pinfo.cols.info = string.sub('hello', 1, 80)
end

--增加协议到Wireshark中
udp_table:add(4444, my_proto)
```
