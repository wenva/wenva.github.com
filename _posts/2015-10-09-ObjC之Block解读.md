---
layout: post
title: "ObjC之Block解读"
date: 2015-10-09
comments: false
categories: OBJC
---

### 1. 类型
根据block在内存中的位置，分为如下三种

* NSGlobalBlock
	* 位于text段
	* 不引用外部成员变量或局部变量（引用全局或静态也是NSGlobalBlock）
	<pre>
void (^block)(int a, int b) = ^(int a, int b){
	//此处除了形参，不能使用外部变量
	int c = a+b;
};</pre>
* NSStackBlock
	* 位于栈内存
	* 在函数中直接通过^{}定义的
	* 不管block是否使用外部变量，都是NSStackBlock
	<pre>
	NSLog(@"block = %@", ^{
		//此处不管是否访问外部变量，都是NSStackBlock
	})</pre>
* NSMallocBlock
	* 位于堆内存
	* 引用外部变量
	* ARC模式下会将block从栈拷贝到堆上，而MRC中需要使用copy
	<pre>
	int c;
void (^block)(int a, int b) = ^(int a, int b){
	//此处引用了外部变量c
	int d = c+a+b;
};</pre>

### 2 引用外部变量(针对NSStackBlock、NSMallocBlock)

#### 2.1 引用外部基础类型变量
<pre>
@interface TestViewController () {
    int _count; //成员变量
}
@end

...

int g_count = 100; //全局变量

- (void)test {
    ....
    
    static int s_count = 100; //静态变量
    int count = 101; //局部变量
    NSLog(@"g_count= %p", &g_count);
    NSLog(@"s_count= %p", &s_count);
	NSLog(@"_count = %p", &_count);
    NSLog(@"count= %p", &count);
    ^{
        NSLog(@"block g_count= %p", &g_count);
        NSLog(@"block s_count= %p", &s_count);
		NSLog(@"block _count = %p", &_count);
        NSLog(@"block count= %p", &count);
    }();
    ...
}
</pre>
输出:
<pre>
2015-10-09 23:09:55.564 BlockTest[64349:778572] g_count= 0x1077d1390
2015-10-09 23:09:55.565 BlockTest[64349:778572] s_count= 0x1077d1394
2015-10-09 23:09:55.565 BlockTest[64349:778572] _count = 0x7fe240ea4478
2015-10-09 23:09:55.565 BlockTest[64349:778572] count= 0x7fff5842ed5c
2015-10-09 23:09:55.565 BlockTest[64349:778572] block g_count= 0x1077d1390
2015-10-09 23:09:55.565 BlockTest[64349:778572] block s_count= 0x1077d1394
2015-10-09 23:09:55.566 BlockTest[64349:778572] block _count = 0x7fe240ea4478
2015-10-09 23:09:55.566 BlockTest[64349:778572] block count= 0x7fff5842ed58
</pre>

* 对于局部变量，block将会对其进行copy
* static变量、全局变量，block不对其进行copy

#### 2.2 外部对象类型变量

##### MRC模式下
* 全局对象、静态对象，在block copy，不会进行retain
* 成员变量，在block copy 不会对成员变量进行retain，`但是会对self进行retain`
* 局部变量，在block copy 会进行retain

##### ARC模式下
* 局部变量，block会copy其指针，并强引用一次
* 静态变量、全局变量会强引用一次
* 当block被释放，则相应的引用减1
* 成员变量，在block copy 不会对成员变量进行retain，`但是会对self进行retain`

### 3. 注意事项
* 与其他objc对象不同，block默认是在栈上分配的，因此需要注意copy
	<pre>
	“As an optimization, block storage starts out on the stack—just like blocks 	themselves do.”</pre>
* NSSet和NSArray 初始化(arrayWithObjects, initWithObjects)只对第一个block进行copy(验证了下字典对象是ok的)
	<pre>
    [NSMutableArray arrayWithObjects:
            ^{ NSLog(@"this is block 1:%i", num); }, //NSMallocBlock
            ^{ NSLog(@"this is block 1:%i", num); }, //NSStackBlock
            nil];</pre>
* 循环引用

 	<pre>
	//如下代码将会导致循环引用
    self.block = ^{
    	//此处对成员变量_testObject1进行了引用，会导致对self进行了retain(参考2.2)
        NSLog(@"block ==========%@", _testObject1);
    };</pre>

	* 此处解决方法有
		* (1) self.block = nil
		* (2) 使用weak或者__unsafe_unretained
		<pre>
		__weak typeof(self) weakSelf = self;
		//__unsafe_unretained typeof(self) weakSelf = self;
	    self.block = ^{
	        NSLog(@"block ==========%@", weakSelf.testObject1);
	    };</pre>
	
