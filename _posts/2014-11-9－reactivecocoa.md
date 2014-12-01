---
layout: post
title: "ReactiveCocoa解析"
date: 2014-11-9
comments: false
---

# ReactiveCocoa 解析


===
## RAC
在ReactiveCocoa中经常使用RAC宏来关联属性和信号，当该信号触发时，相应的属性也会发生变化，那么这个是怎么实现的？

#### 例子
<pre>
///  RAC(self, objectProperty) = objectSignal;
///  RAC(self, stringProperty, @"foobar") = stringSignal;
///  RAC(self, integerProperty, @42) = integerSignal;
</pre>

#### 剖析

##### （1）宏
我们查看源码可以很容易发现RAC宏定义如下:
<pre>
#define RAC(TARGET, ...) \
    metamacro_if_eq(1, metamacro_argcount(__VA_ARGS__)) \
        (RAC_(TARGET, __VA_ARGS__, nil)) \
        (RAC_(TARGET, __VA_ARGS__))
</pre>
对于上面的宏我们需要清楚```metamacro_if_eq```和```metamacro_argcount```两个宏作用

* metamacro_argcount - 获取参数个数
<pre>
#define metamacro_argcount(...) \
        metamacro_at(20, __VA_ARGS__, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
        
#define metamacro_at(N, ...) \
        metamacro_concat(metamacro_at, N)(__VA_ARGS__) //得到的值metamacro_at20
        
#define metamacro_at20(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, _11, _12, _13, _14, _15, _16, _17, _18, _19, ...) metamacro_head(__VA_ARGS__) //取可变参数中的第一个

#define metamacro_head(...) \
        metamacro_head_(__VA_ARGS__, 0)
        
#define metamacro_head_(FIRST, ...) FIRST //取第一个参数
</pre>
PS:通过上述过程可以知道，其原理是将可变参数插入到已有的序列[20到1]的头部，导致序列后推，取出的第21个参数就是插入的参数个数.

* metamacro_if_eq - metamacro_if_eq(A, B)(true)(false)
<pre>
#define metamacro_if_eq(A, B) \
        metamacro_concat(metamacro_if_eq, A)(B) //metamacro_concat负责连接参数
        
#define metamacro_if_eq0(VALUE) \
    metamacro_concat(metamacro_if_eq0_, VALUE)
#define metamacro_if_eq1(VALUE) metamacro_if_eq0(metamacro_dec(VALUE)) //metamacro_dec将VALUE值-1
#define metamacro_if_eq2(VALUE) metamacro_if_eq1(metamacro_dec(VALUE))
...
//同时递减A和B，直到A为0，根据B的值得出对应的宏metamacro_if_eq0_(B-A)

#define metamacro_if_eq0_0(...) __VA_ARGS__ metamacro_consume_
#define metamacro_if_eq0_1(...) metamacro_expand_
#define metamacro_if_eq0_2(...) metamacro_expand_
...     
</pre>
PS: 原理:同时递减A和B，直到A为0，根据递减后B的值得出对应的参数metamacro_if_eq0_(B-A)
	* 当A=B则为metamacro_if_eq0_0
	* 当A<B则为metamacro_if_eq0_X
	
根据上述宏我们可以知道，当A=B，则:
<pre>
#define metamacro_consume_(...)

metamacro_if_eq(A, B)(true)(false) => true metamacro_consume_(false) => true
</pre>

当A < B， 则:
<pre>
#define metamacro_expand_(...) __VA_ARGS__

metamacro_if_eq(A, B)(true)(false) => metamacro_expand_(false) => false
</pre>

有了以上的基础，我们继续分析RAC_宏

<pre>
#define RAC_(TARGET, KEYPATH, NILVALUE) \
    [[RACSubscriptingAssignmentTrampoline alloc] initWithTarget:(TARGET) nilValue:(NILVALUE)][@keypath(TARGET, KEYPATH)]
    
#define keypath(...) \
    metamacro_if_eq(1, metamacro_argcount(__VA_ARGS__))(keypath1(__VA_ARGS__))(keypath2(__VA_ARGS__))

#define keypath1(PATH) \
    (((void)(NO && ((void)PATH, NO)), strchr(# PATH, '.') + 1)) //#将参数转成字符串

#define keypath2(OBJ, PATH) \
    (((void)(NO && ((void)OBJ.PATH, NO)), # PATH)) //取#PATH
</pre>
PS: 通过上述宏，我们可以知道知道最终的形式:```object[@"key"] = signal```

上述语法是类似与字典操作:
<pre>
id value = dictionary[@"key"]; 
dictionary[@"key"] = newObj;
</pre>
其真正是调用:
<pre>
- (id)objectForKeyedSubscript: (id <NSCopying>)key; 
- (void)setObject: (id)anObject forKeyedSubscript: (id <NSCopying>)aKey;
</pre>
PS: 如果自定义的类想要实现[@"key"]方式访问，可以自定义setObject:forKeyedSubscript:方法

##### （2）KVC
通过第一阶段宏的分析，我们可以了解到最终是通过```setObject:forKeyedSubscript:```方法来执行操作，继续分析，RACSubscriptingAssignmentTrampoline类中我们可以看到```setObject:forKeyedSubscript:```的定义:
<pre>
- (void)setObject:(RACSignal *)signal forKeyedSubscript:(NSString *)keyPath {
	[signal setKeyPath:keyPath onObject:self.target nilValue:self.nilValue];
}
</pre>
对应于```RAC(self, objectProperty) = objectSignal```来说, keyPath=objectProperty, signal=objectSignal，即将keyPath和target设入到Signal中.我们继续分析RACSignal的setKeyPath:onObject:nilValue方法
<pre>
- (RACDisposable *)setKeyPath:(NSString *)keyPath onObject:(NSObject *)object nilValue:(id)nilValue {
	...
	RACDisposable *subscriptionDisposable = [self subscribeNext:^(id x) {
		// Possibly spec, possibly compiler bug, but this __bridge cast does not
		// result in a retain here, effectively an invisible __unsafe_unretained
		// qualifier. Using objc_precise_lifetime gives the __strong reference
		// desired. The explicit use of __strong is strictly defensive.
		__strong NSObject *object __attribute__((objc_precise_lifetime)) = (__bridge __strong id)objectPtr;
		<font color="00ff00">[object setValue:x ?: nilValue forKeyPath:keyPath];</font>
	} error:^(NSError *error) {
		__strong NSObject *object __attribute__((objc_precise_lifetime)) = (__bridge __strong id)objectPtr;

		NSCAssert(NO, @"Received error from %@ in binding for key path \"%@\" on %@: %@", self, keyPath, object, error);

		// Log the error if we're running with assertions disabled.
		NSLog(@"Received error from %@ in binding for key path \"%@\" on %@: %@", self, keyPath, object, error);

		[disposable dispose];
	} completed:^{
		[disposable dispose];
	}];
	...
}
</pre>
通过上述代码我们可以了解到最终是通过KVC来对属性进行赋值更新的.

====
## RACCommand
#### objc对象关联
在了解rac_command之前，先了解下objc关联，```关联是指把两个对象相互关联起来，使得其中的一个对象作为另外一个对象的一部分```，分别使用objc_setAssociatedObject和objc_getAssociatedObject来设置或访问关联对象.
<pre>
OBJC_EXPORT id objc_getAssociatedObject(id object, const void *key)
OBJC_EXPORT void objc_setAssociatedObject(id object, const void *key, id value, objc_AssociationPolicy policy)

enum {
    OBJC_ASSOCIATION_ASSIGN = 0,           /**< Specifies a weak reference to the associated object. */
    OBJC_ASSOCIATION_RETAIN_NONATOMIC = 1, /**< Specifies a strong reference to the associated object. 
                                            *   The association is not made atomically. */
    OBJC_ASSOCIATION_COPY_NONATOMIC = 3,   /**< Specifies that the associated object is copied. 
                                            *   The association is not made atomically. */
    OBJC_ASSOCIATION_RETAIN = 01401,       /**< Specifies a strong reference to the associated object.
                                            *   The association is made atomically. */
    OBJC_ASSOCIATION_COPY = 01403          /**< Specifies that the associated object is copied.
                                            *   The association is made atomically. */
};

/// Type to specify the behavior of an association.
typedef uintptr_t objc_AssociationPolicy;
</pre>
#### rac_command
通过关联将对象RACCommand对象关联到UIButton等对象中.
<pre>
- (RACCommand *)rac_command {
	return objc_getAssociatedObject(self, UIButtonRACCommandKey);
}

- (void)setRac_command:(RACCommand *)command {
	objc_setAssociatedObject(self, UIButtonRACCommandKey, command, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
	...
}
</pre>
PS:另外，setRac_command中还绑定UIButton等的Touch事件来触发RACCommand的execute方法