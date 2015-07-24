---
layout: post
title: "Objective-C之runtime"
date: 2015-07-24
comments: false
categories: iOS
---

![image](http://cc.cocimg.com/api/uploads/20141224/1419385503900732.jpg)

* 从左到右：实例、对象、类（对象是类的实例化，实例是对象的实例化）
* 理解self
	* 在类方法中，self指向类对象地址（即上图中间部分）
	* 在实例方法中，self指向实例地址（即上图左边部分）
* 类class方法
<pre>
+ (Class)class {
    return self; //指向上图中间部分
}
</pre>
* 对象class方法
<pre>
- (Class)class {
    return object_getClass(self); //指向上图中间部分
}
</pre>
PS: `[[NSObject new] class]` `[NSObject class]` `[[NSObject class] class]`都是指向同一地址
* 
