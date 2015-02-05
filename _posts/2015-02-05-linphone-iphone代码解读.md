---
layout: post
title: "linphone-iphone代码解读"
date: 2015-02-05
comments: false
---
# linphone-iphone代码解读
February 5, 2015

## [流程](http://fossies.org/dox/linphone-3.7.0)
### 1. 初始化startLibLinphone
* （1）模块初始化，包含mediastreamer2、ilbc、silk、amr、x264、h264、bcg729
* （2）创建linphone core(createLinphoneCore)
	<pre>
		theLinphoneCore = linphone_core_new_with_config (&linphonec_vtable
										 ,configDb
										 ,self /* user_data */);
	</pre>
	* linphonec_vtable为所有回调接口，包含:
		* call 状态改变回调
		* 
* （3）初始化audio session

