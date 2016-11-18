# iOS静态库的链接与加载

引言：研究iOS静态库的链接与加载是源自这个问题：`为何引用同一个SDK，在真机可以编译成功，而在模拟器在出现duplicate symbol?`,一时间无法理解，按道理说如果出现duplicate symbol，说明代码中应该有重复定义的部分，而为何真机又ok，难道真机屏蔽了部分代码？带着这些疑问和猜想，进行如下实验

### 实验
实践才是检验真理的唯一标准

* Demo
	* Testlib1
		<pre>
		void hello() {
    		printf("Testlib1: hello\n");
		}
		void hello2() {
    		printf("Testlib1: hello1\n");
		}</pre>
	* Testlib2
		<pre>
		void hello() {
    		printf("Testlib2: hello\n");
		}
		void hello2() {
    		printf("Testlib2: hello2\n");
		}</pre>

PS: 以上是测试DEMO工程框架, Demo为主工程，包含2个静态库工程：Testlib1, Testlib2


|编号|CPU架构|链接标识|库链接顺序|测试代码|Symbol|输出|备注
|:--|:--
|1|arm64|空|Testlib1.framework<br>Testlib2.framework|hello()|T \_hello<br>T \_hello1|Testlib1: hello|原始
|2|arm64|空|Testlib2.framework<br>Testlib1.framework|hello()|T \_hello<br>T \_hello2|Testlib2: hello|调整库链接顺序
|3|arm64|空|Testlib1.framework<br>Testlib2.framework|hello();hello1()|T \_hello<br>T \_hello1|Testlib1: hello;Testlib1: hello1|打印hello1
|4|arm64|空|Testlib1.framework<br>Testlib2.framework|hello();hello2()|T \_hello<br>T \_hello1<br>T _hello2|Testlib2: hello;Testlib2: hello2|打印hello2
|5|arm64|-all_load|Testlib1.framework<br>Testlib2.framework|hello();hello2()|报错：duplicate symbol _hello||链接标识+打印hello2
|11|x86_64|空|Testlib1.framework<br>Testlib2.framework|hello()|T \_hello<br>T \_hello1|Testlib1: hello|模拟器
|12|x86_64|空|Testlib2.framework<br>Testlib1.framework|hello()|T \_hello<br>T \_hello2|Testlib2: hello|模拟器+调整库链接顺序
|13|x86_64|空|Testlib1.framework<br>Testlib2.framework|hello();hello1()|T \_hello<br>T \_hello1|Testlib1: hello;Testlib1: hello1|模拟器+打印hello1
|14|x86_64|空|Testlib1.framework<br>Testlib2.framework|hello();hello2()|报错：duplicate symbol _hello||模拟器+打印hello2

### 结论
* 库加载是通过配置的顺序进行加载，当发现需要调用的接口都已经定义，则不在继续加载，否则继续加载（根据1、2、3得出）
* 后者加载的接口会覆盖前面库的接口（根据4得出）
* 模拟器下不允许重复定义（根据14得出）
* -all_load下不允许接口重定义（根据5得出）


### 总结
通过上述结论，可以更好的解释：`为何引用同一个SDK，在真机可以编译成功，而在模拟器在出现duplicate symbol?`，当然以上测试是在XCode 8.0及iPhone 5s 10.0.1上进行的.我并未找到官方说明，若哪位童鞋有找到apple文档，可以告知我.