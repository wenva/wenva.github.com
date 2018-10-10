---
layout: post
title: "awesome-ios-develop"
date: 2015-06-25
comments: false
categories: IOS
---
下文是我在开发iOS APP两年后的一些经验总结.

* Objective C 代码规范
	* 采用骆驼峰法命名
	* 类名、变量全拼，尽量不缩写
	* 类成员变量使用_开头
	* 类名、协议名首字母大写	
	* 更多详情参考[苹果规范](https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.pdf)
	
* 采用git来做版本管理
* gitignore必不可少，否则会多出很多冲突
* 善用Github，如follow、starred、fork

* 善用Code Snippet
	* 将最常用的代码端放入到snippet中，并定义尽量少的快捷键(一般2个)，如bg - 后台线程，fg - 前台线程
	* 将这些Code Snippet同步到github
	
* 使用独立的log系统（如CocoaLumberjack），而不是用系统的NSLog
* 善用宏，将需要大量使用的接口调用用宏替换
<pre>
#define IMG(__name) [UIImage imageNamed:__name]
#define RGBA(R, G, B, A) [UIColor colorWithRed:R/255.0 green:G/255.0 blue:B/255.0 alpha:A]
#define RGB(R, G, B) RGBA(R, G, B, 1)
</pre>
* 当第三方库中有对Cocoa SDK类进行扩展时，注意添加-ObjC链接flag

### 调试和发布
* 真机调试，Certificates、Identifiers、Provisioning Profile必不可少
* 使用TestFlight进行内部分发，支持20个内部账号和1000个外部账号
* 使用iTunes Connect来管理和发布APP
* 利用xcode查看UIImage对象的图
![image](http://7ximmr.com1.z0.glb.clouddn.com/xcode_debug_show_uiimage.jpg)
