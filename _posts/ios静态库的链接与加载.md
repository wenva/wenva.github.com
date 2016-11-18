# iOS静态库的链接与加载

引言：研究iOS静态库的链接与加载是源自这个问题：`为何引用同一个SDK，在真机可以编译成功，而在模拟器在出现duplicate symbol?`,一时间无法理解，按道理说如果出现duplicate symbol，说明代码中应该有重复定义的部分，而为何真机又ok，难道真机屏蔽了部分代码？带着这些疑问和猜想，进行如下实验

### 实验
实践才是检验真理的唯一标准

* Demo
	* Testlib1
		<pre>
		void hello();
		void hello1();</pre>
	* Testlib2
		<pre>
		void hello();
		void hello2();</pre>

PS: 以上的测试DEMO, Demo为主工程包含2个静态库工程：Testlib1, Testlib2


|环境|链接标识(Other Linker Flags)|库链接顺序(Link Binary With Libraries)|测试代码|输出|备注
|:--|:--
|真机|空|Testlib1.framework<br>Testlib2.framework|hello()|