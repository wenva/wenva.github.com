---
layout: post
title: "UITabbarItem图标要求"
date: 2014-12-22
comments: false
categories: iOS
---
![image](http://www.2cto.com/uploadfile/2012/0915/20120915045908604.png)

* 图标需要同时存在透明和非透明色
* 单色的非透明色将被全部覆盖，选中为蓝色，非选中为灰色


## 自定义选中图

iOS7.0 后提供自定义选中图

<pre>
@property(nonatomic,retain) UIImage *selectedImage NS_AVAILABLE_IOS(7_0);
</pre>
对于selectedImage是需要设置渲染模式（同样针对image），可以在API文档中查看
<pre>
By default, the actual selected image is automatically created from the alpha values in the source image. To prevent system coloring, provide images with UIImageRenderingModeAlwaysOriginal.
</pre>

于是我们可以通过UIImage提供的imageWithRenderingMode来进行设置

### Demo

<pre>
    self.tabBar.backgroundImage = IMG(@"tabbar_background");
    [self.tabBar setShadowImage:[[UIImage alloc] init]];// 去除边框

    NSArray* images = @[@"tabbar_invatation_icon", @"tabbar_home_icon", @"tabbar_monitor_icon"];
    NSArray* selectedImages = @[@"tabbar_invatation_icon_h", @"tabbar_home_icon_h", @"tabbar_monitor_icon_h"];
    NSArray* titles = @[@"invatation", @"home", @"monitor"];
    int i = 0;
    for (UITabBarItem* item in self.tabBar.items) {
        item.image = [[UIImage imageNamed:images[i]] imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal];
        item.selectedImage = [[UIImage imageNamed:selectedImages[i]] imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal];
        item.title = GET_STRING(titles[i]);
        i++;
    }
</pre>

