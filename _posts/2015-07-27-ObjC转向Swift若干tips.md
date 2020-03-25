---
layout: post
title: "ObjC转向Swift若干tips"
date: 2015-07-27
comments: false
categories: IOS
---
* 不分头文件和实现文件，而是集合到.swift文件
* 类型对象化（类似于java） Int、Float、Double、Bool、Character
* let 定义常量； len pi = 3.14
* var hello :NSString ?
	* var 定义变量`var hello :NSString = @"1212"`
	* : 指定变量类型
	* ? 表示optional，即该变量可能为nil; 调用时必须加? 如 `hello?.length`
	* ! 表示该变量一定不为nil，否则crash

* @"hello"不存在了,变回了"hello" 如`var hello :NSString = "hello"`
* 可以使用+来拼接字符串 `"hello"+"world"`
* 使用\()可以在字符串插入变量 `let lang = "swift"; "hello \(lang) world"`
* class 定义类
* func 定义函数
	* func xxxx(xxx ...) -> 返回类型
	 
* println 带换行的print
* as 类型转换 “当作”
