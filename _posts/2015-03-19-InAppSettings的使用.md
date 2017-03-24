---
layout: post
title: "InAppSettings的使用"
date: 2015-03-19
comments: false
categories: OBJC
---

InAppSettings为APP提供了Settings的快捷化构建，只需少量代码就可以实现复杂的设置界面，下面来阐述如何使用InAppSettings.

## 使用
* 包含头文件
<pre>
\#import "IASKAppSettingsViewController.h"
</pre>
* 添加Settings.bundle
<pre>
"新建"->"Resource"->"Settings Bundle"
</pre>
* 初始化Controller并呈现
<pre>
IASKAppSettingsViewController* vc = [[IASKAppSettingsViewController alloc] initWithNibName:@"IASKAppSettingsView" bundle:nil];
UINavigationController *navController = [[UINavigationController alloc] initWithRootViewController:vc];
[self presentViewController:navController animated:YES completion:^{
    
}];
</pre>

## Settings.bundle
Settings.bundle至少包含一个Root.plist
