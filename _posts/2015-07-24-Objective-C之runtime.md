---
layout: post
title: "Objective-C之runtime"
date: 2015-07-24
comments: false
categories: OBJC
---

![image](http://cc.cocimg.com/api/uploads/20141224/1419385503900732.jpg)

#### 1. 从左到右：实例、对象、类
* 对象是类的实例化，实例是对象的实例化

#### 2. 理解self
* 在类方法中，self指向类对象地址（即上图中间部分）
* 在实例方法中，self指向实例地址（即上图左边部分）

#### 3. 理解super
* 编译器定的符号（类似while）强调的是调用父类方法

#### 4. class方法
<pre>
+ (Class)class {
    return self; //指向上图中间部分
}
</pre>
<pre>
- (Class)class {
    return object_getClass(self); //指向上图中间部分
}
</pre>
PS: `[[NSObject new] class]` `[NSObject class]` `[[NSObject class] class]`都是指向同一地址

#### 5. isKindOf方法
<pre>
- (BOOL)isKindOf:aClass
{
    Class cls;
    for (cls = isa; cls; cls = cls->superclass) 
        if (cls == (Class)aClass)
            return YES;
    return NO;
}
</pre>

#### 6. isMemberOf方法 - 即isKindOf的部分条件
<pre>
- (BOOL)isMemberOf:aClass
{
    return isa == (Class)aClass;
}
</pre>

#### 7. 对class取指针,并强转成NSObject对象 （等效于 对该class实例化）
<pre>
id cls = [NSString class];
void* p = &cls;
[(__bridge NSString*)p class];
</pre>
PS: 如上代码正常返回，并不会crash，原因在于
<pre>
typedef struct objc_object *id;
struct objc_object {
    Class isa;
};
</pre>

![image](http://7ximmr.com1.z0.glb.clouddn.com/objc_runtime_1.jpg)
