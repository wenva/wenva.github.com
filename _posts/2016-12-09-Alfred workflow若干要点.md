---
layout: post
title: "Alfred workflow若干要点"
date: 2016-12-09
comments: false
categories: 工具
---

Alfred workflow真是个神器，自从上手后，就割舍不掉，目前很多原来繁琐的动作都可以通过简单的方式进行，虽然网上已经有很多别人写好的workflow，但总是不够用，毕竟各自的偷懒点不同，因此就必须会workflow的编写，本文将为大家介绍最为常用的技巧.


### 工作模式
 Alfred workflow，顾名思义是以流的方式来进行工作的，从`输入 -> 动作 -> 输出`，非常开放，可以说是一个精妙的设计.
 
* 输入
	* Triggers - 触发器
		* Hotkeys - 快捷键
		* Remote - 远程
		* ...
	* Inputs - 输入源
		* Keywords - 关键字
		* Script Filter - 脚本过滤器
		* ...
* 动作
	* Actions - 动作
		* System Command - 系统命令
		* Launch App - 运行程序
		* Open URL - 打开网页
		* Run Script - 运行脚本
		* ...
* 输出
	* Outputs - 输出
		* Post Notification - 系统通知
		* Copy To Clipboard - 复制到系统粘贴板
		
### 要点

##### 1. 参数传递 - 通过标准输入输出来实现

* 第一级一般是用户输入的，如在Keywords输入源中可以选择是否带参数
* 上一级的结果直接输出到stdout作为下一级的参数，下一级可以通过{query}来获取

例如：我需要把hello alfred输出到下一级
<pre>
echo -n "hello alfred" 
</pre>
PS: 此处必须加-n，否则默认是带换行符

##### 2. 脚本过滤器（Script Filter）

有时候你需要直接在alfred的下拉列表中展现结果（非常拉风），你就需要用到Script Filter.
![image](https://www.alfredapp.com/help/workflows/inputs/script-filter/json-example.png)

Alfred是通过XML来展现输出，XML格式如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<items>
    <item valid="YES">
        <title>标题</title>
        <subtitle>子标题</subtitle>
		<arg>下一级参数</arg>
		...
    </item>
	...
</items>
```
PS：Alfred 3.0引入了JSON作为输出

```
{"items": [
    {
        "title": "标题",
        "subtitle": "子标题",
        "arg": "下一级参数",
        ...
    }
]}
```

|参数|说明|备注|
|:--|:--
|title|标题|
|subtitle|子标题|
|arg|下一级参数|当选择此项后，会将此参数作为输出传递给下一级

更多参数详见[这里](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/)


下面是我编写查看本机ip的DEMO

```
ip=$(ifconfig|sed -n '/en/,/status/p'|awk '/broadcast/{print $2}')

cat << EOF
<?xml version="1.0" encoding="UTF-8"?>
<items>
    <item valid="YES">
        	<title>$ip</title>
		<arg>$ip</arg>
    </item>
</items>
EOF
```
