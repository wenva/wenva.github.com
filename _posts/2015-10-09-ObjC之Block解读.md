---
layout: post
title: "ObjC之Block解读"
date: 2015-10-09
comments: false
categories: ios
---

### 类型
* NSGlobalBlock
	* 位于text段
	* 不引用外部变量
	<pre>
void (^block)(int a, int b) = ^(int a, int b){
	//此处不能对除了形参，不能对使用外部变量
	int c = a+b;
};
</pre>
* NSStackBlock
	* 位于栈内存
	* 在函数中直接通过^{}定义的
	* 不管block是否使用外部变量，都是NSStackBlock
	<pre>
	NSLog(@"block = %@", ^{
		//此处不管是否对外部变量，都是NSStackBlock
	})
</pre>
* NSMallocBlock
	* 位于堆内存
	* 引用外部变量
	* ARC模式下会将block从栈拷贝到堆上，而MRC中需要使用copy
	<pre>
	int c;
void (^block)(int a, int b) = ^(int a, int b){
	//此处引用了外部变量c
	int d = c+a+b;
};
</pre>

### 外部变量
* static变量、全局变量，在block中将访问器内存