---
layout: post
title: "MacOSX下编译linphone"
date: 2015-02-02
comments: false
categories: iOS
---
Linphone是一个开源的VOIP框架，利用它提供的库能够快速构建一个VOIP的客户端. 虽然Linphone提供了iPhone版源码，但编译它还是遇到了不少问题，现将记录于此.

## 依赖库
* cunit - c单元测试框架库
* silk - skype自己的音频解码器
* webrtc - 实时网页即时通信，是一个支持网页浏览器进行实时语音对话或视频对话的API
* x264 - 进行H.264/MPEG-4 AVC的视频编码，而不是作为解码器（decoder）之用.
* polarssl - 最小巧的ssl代码库。高效、便于移植和集成。尤其适合嵌入式应用
* speex - Speex是一套主要针对语音的开源免费，无专利保护的音频压缩格式。Speex工程着力于通过提供一个可以替代高性能语音编解码来降低语音应用输入门槛 
* srtp - VoIP网络很不安全，这也是限制VoIP发展的一个考虑因素。为了提供一种策略满足VoIP的安全，SRTP应运而生。所谓SRTP，即安全实时传输协议(Secure Real-time Transport
Protocol)，其是在实时传输协议(Real-time Transport Protocol)基础上所定义的一个协
议，旨在为单播和多播应用程序中的实时传输协议的数据提供加密、消息认证、完整性保
证和重放保护。
* ImageMagick - ImageMagick是一套功能强大、稳定而且开源的工具集和开发包，可以用来读、写和处理超过89种基本格式的图片文件，包括流行的TIFF、JPEG、GIF、 PNG、PDF以及PhotoCD等格式。
* gsm - gsm音频编解码
* libtool - 封装了不同平台动态链接库的差异，为开发人员提供统一接口
* bcg729 - g729语音编解码库
* belle-sip - SIP协议栈
* amr - AMR即自适应多速率压缩（Adaptive multi-Rate compression）是一个使语音编码最优化的专利
* ilbc - iLBC是一种专为包交换网络通信设计的编解码，优于目前流行的G.729、G.723.1，对丢包进行了特有处理，即使在丢包率 相当高的网络环境下，仍可获得非常清晰的语音效果。
* openh264 - 思科的h264编解码器
* antlr3 - 语言识别的一个工具 (ANother Tool for Language Recognition ) 是一种语言工具，它提供了一个框架，可以通过包含 Java, C++, 或 C# 动作（action）的语法描述来构造语言识别器，编译器和解释器。
	* 安装方法:
	<pre>
	下载jar文件，并拷贝到/usr/share/java目录下
	sudo cp antlr-3.4-complete.jar /usr/share/java/antlr.jar
	</pre>
	** 注意:必须是3.4，否则可能会报_empty不存在 **


## Build 问题汇总
### 1. error: C compiler cannot create executables
##### 问题
<pre>
checking whether the C compiler works... no
configure: error: in `/Users/starnet/Projects/linphone-iphone/submodules/build-i386-apple-darwin/externals/polarssl':
configure: error: C compiler cannot create executables
</pre>
##### 分析
<pre>
clang -std=c99 -Qunused-arguments -Wno-unknown-warning-option -Wno-unused-command-line-argument-hard-error-in-future  -arch i386  -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk -mios-simulator-version-min=4.0 -DTARGET_OS_IPHONE=1 -D__IOS -fms-extensions -Dsha256=polarssl_sha256  -Dasm=__asm hello.c 
ld: -pie can only be used when targeting iOS 4.2 or later
clang: error: linker command failed with exit code 1 (use -v to see invocation)
</pre>
修改上述ios-simulator-version-min=4.2即可以通过编译

##### 处理
于是修改submodules/build/iphone-config.site的SDK_VERSION
<pre>
SDK_VERSION_MAJOR=4                                                              
SDK_VERSION=4.2   
</pre>

### 2. aclocal: error: aclocal: file 'm4/lt~obsolete.m4' does not exist
##### 问题
<pre>
-e  Running autogen for msopus in /Users/starnet/Projects/linphone-iphone/submodules/build/..//externals/opus 
cd /Users/starnet/Projects/linphone-iphone/submodules/build/..//externals/opus && ./autogen.sh
Updating build configuration files, please wait....
aclocal: error: aclocal: file 'm4/lt~obsolete.m4' does not exist
autoreconf: aclocal failed with exit status: 1
</pre>

##### 分析
分析发现/opt/local/share/aclocal/lt~obsolete.m4路径不存在，发现/usr/local/share/aclocal/存在，于是建立软连接
	
##### 处理
<pre>
sudo ln -s /usr/local/share/aclocal /opt/local/share/
</pre>

### 3. configure: error: GNU gettext tools not found; required for intltool
##### 问题
<pre>
configure: error: GNU gettext tools not found; required for intltool
</pre>
##### 分析
未安装gettext

##### 处理
<pre>
sudo brew install gettext
sudo ln -s /usr/local/Cellar/gettext/0.19.3_1/bin/msgmerge /usr/local/bin/
sudo ln -s /usr/local/Cellar/gettext/0.19.3_1/bin/msgfmt /usr/local/bin/
sudo ln -s /usr/local/Cellar/gettext/0.19.3_1/bin/xgettext /usr/local/bin/
</pre>
	
### 4. 'CoreFoundation/CFUserNotification.h' file not found
##### 问题
<pre>
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks/CFNetwork.framework/Headers/CFHost.h:22:
/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks/CoreFoundation.framework/Headers/CoreFoundation.h:92:10: fatal error: 
      'CoreFoundation/CFUserNotification.h' file not found
#include <CoreFoundation/CFUserNotification.h>
</pre>
	
##### 分析
查看CoreFoundation.h文件，发现TARGET_OS_IPHONE被重置为0，经过寻找是由于CFBase.h中调用的TargetConditionals.h是来自于MacOSX10.10的SDK下面，后面发现是由于指定了C_INCLUDE_PATH
<pre>
declare -x C_INCLUDE_PATH="/Developer//Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.10.sdk/usr/include/"
</pre>
##### 处理
直接export C_INCLUDE_PATH = ""
	
### 5. error: Libtool library used but 'LIBTOOL' is undefined
##### 问题
<pre>
CUnit/Sources/Automated/Makefile.am:3: error: Libtool library used but 'LIBTOOL' is undefined
CUnit/Sources/Automated/Makefile.am:3:   The usual way to define 'LIBTOOL' is to add 'LT_INIT'
CUnit/Sources/Automated/Makefile.am:3:   to 'configure.in' and run 'aclocal' and 'autoconf' again.
CUnit/Sources/Automated/Makefile.am:3:   If 'LT_INIT' is in 'configure.in', make sure
</pre>
##### 分析
aclocal是一个perl脚本程序，扫描configure.ac来创建aclocal.m4文件，以供autoconf来生成configure文件
'LIBTOOL' is undefined是由于aclocal找不到libtool宏，原因可能是没安装libtool或路径不对，aclocal -I可以制定m4文件路径
	
##### 处理
拷贝libtool下得m4文件到aclocal下
<pre>
sudo cp /usr/local/Cellar/libtool/2.4.2/share/aclocal/* /opt/local/share/aclocal/
</pre>

### 6. syntax error near unexpected token `am__api_version='1.14''

##### 问题
<pre>
/Users/starnet/Projects/linphone-iphone/submodules/build/..//belle-sip/configure: line 2637: syntax error near unexpected token \`am__api_version='1.14''
/Users/starnet/Projects/linphone-iphone/submodules/build/..//belle-sip/configure: line 2637: `am__api_version='1.14''
builders.d/belle-sip.mk:27: recipe for target '/Users/starnet/Projects/linphone-iphone/submodules/build/../build-i386-apple-darwin/belle-sip/Makefile' failed
make[1]: *** [/Users/starnet/Projects/linphone-iphone/submodules/build/../build-i386-apple-darwin/belle-sip/Makefile] Error 2
</pre>
	
##### 分析
测试发现是由于PKG_PROG_PKG_CONFIG() 未定义导致的，而PKG_PROG_PKG_CONFIG() 是存在于pkg.m4中（由pkg-config提供）
	
##### 处理
通过aclocal -I或者将pkg.m4拷贝到aclocal的目录下
<pre>
aclocal --print-ac-dir #可以查看aclocal目录
sudo cp /usr/local/Cellar/pkg-config/0.28/share/aclocal/pkg.m4 /opt/local/share/aclocal/
</pre>	

### 7. syntax error near unexpected token `MSGFMT,'
##### 问题
<pre>
/Users/starnet/Projects/linphone-iphone/submodules/build/..//linphone/mediastreamer2/configure: line 17534: syntax error near unexpected token `MSGFMT,'
/Users/starnet/Projects/linphone-iphone/submodules/build/..//linphone/mediastreamer2/configure: line 17534: `        AM_PATH_PROG_WITH_TEST(MSGFMT, msgfmt,'
configure: error: /Users/starnet/Projects/linphone-iphone/submodules/build/..//linphone/mediastreamer2/configure failed for mediastreamer2
builder-iphone-os.mk:173: recipe for target '/Users/starnet/Projects/linphone-iphone/submodules/build/../build-i386-apple-darwin/linphone/Makefile' failed
make[1]: *** [/Users/starnet/Projects/linphone-iphone/submodules/build/../build-i386-apple-darwin/linphone/Makefile] Error 2
</pre>

##### 分析
测试发现是AM_PATH_PROG_WITH_TEST未定义，这个是在gettext的m4文件中定义

##### 处理
拷贝m4到aclocal下
<pre>
sudo cp /usr/local/Cellar/gettext/0.19.3_1/share/aclocal/* /opt/local/share/aclocal
</pre>

### 8. ld: illegal text-relocation to '_vp8_dequant_idct_add_mmx'
##### 问题
<pre>
ld: illegal text-relocation to '_vp8_dequant_idct_add_mmx' in /Users/starnet/Projects/linphone-iphone/liblinphone-sdk/i386-apple-darwin/lib/libvpx.a(dequantize_mmx.asm.o) from '_vp8_dequant_idct_add_mmx' in /Users/starnet/Projects/linphone-iphone/liblinphone-sdk/i386-apple-darwin/lib/libvpx.a(dequantize_mmx.asm.o) for architecture i386
clang: error: linker command failed with exit code 1 (use -v to see invocation)
</pre>

##### 分析
[这里](http://stackoverflow.com/questions/6650178/illegal-text-reloc-to-non-lazy-ptr-error-while-building-in-xcode-4-with-libav-l)有关于illegal text-relocation的说明
大致意思：当一个全局变量被编译到动态库中，而第三方asm代码需要引用该变量时，连接器会把相对地址付给相应引用，当他们处于一个连接单元时，则不会有问题，当不同单元则就会出问题；应该是连接器的一个bug

##### 处理
(1) 编辑linphone/mediastreamer2/tester/Makefile.am, 为AM_LDFLAGS添加-read_only_relocs suppress
<pre>
 AM_LDFLAGS=-no-undefined -export-dynamic -read_only_relocs suppress
</pre>
(2) 编辑linphone/coreapi/Makefile.am
<pre>
AM_LDFLAGS= -read_only_relocs suppress
</pre>

### 9. extract-cfile.awk无法下载
##### 问题
<pre>
/usr/local/bin/wget --no-check-certificate http://www.webrtc.org/ilbc-freeware/ilbc-source-code-and-utili/ilbc-utilities/extract-cfile.awk -O extract-cfile.awk
--2015-02-04 12:59:41--  http://www.webrtc.org/ilbc-freeware/ilbc-source-code-and-utili/ilbc-utilities/extract-cfile.awk
Resolving www.webrtc.org... 74.125.23.121
Connecting to www.webrtc.org|74.125.23.121|:80... 
</pre>
##### 分析
链接不存在
##### 处理
到www.ilbcfreeware.org下载extract-cfile.txt，拷贝到上传到可用的服务器，这里我上传到github，地址https://github.com/wenva/wenva.github.com/raw/master/resource/extract-cfile.awk
编辑submodules/libilbc-rfc3951/downloads/Makefile.am
<pre>
extract_script = extract-cfile.awk
extract_script_url = https://github.com/wenva/wenva.github.com/raw/master/resource/$(extract_script)
</pre>

### 10. No working C compiler found.
##### 问题
<pre>
./configure --prefix=/Users/starnet/Projects/linphone-iphone/submodules/build/..//../liblinphone-sdk/i386-apple-darwin  --host=i386-apple-darwin --enable-static --enable-pic --cross-prefix=$SDK_BIN_PATH/ --extra-ldflags="$COMMON_FLAGS" --extra-cflags="$COMMON_FLAGS "
Loading config.site for iPhone platform=Simulator version=4.2
/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator8.1.sdk
/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk
Selecting SDK path = /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk
No working C compiler found.
</pre>
##### 分析
查看configure文件
<pre>
...
if $cc_cmd >conftest.log 2>&1; then                                          
...
</pre>
即结果导入conftest.log, 发现如下
<pre>
clang: error: unknown argument: '-falign-loops=16' 
</pre>
即clang不支持-falign-loops
##### 处理
删除submodules/build-i386-apple-darwin/externals/x264
编辑submodules/externals/x264/configure，去除-falign-loops
<pre>
457     darwin*)                                                                     
458         SYS="MACOSX"                                                             
459  #       CFLAGS="$CFLAGS -falign-loops=16"                                       
460         libm="-lm"         
</pre>

### 11. compile: unable to infer tagged configuration
##### 问题
<pre>
libtool: compile: unable to infer tagged configuration
libtool: compile: specify a tag with `--tag'
Makefile:1039: recipe for target 'backgroundtask.lo' failed
make[1]: *** [backgroundtask.lo] Error 1
</pre>

##### 分析
如果使用的compiler不是gcc, libtool会认错，需要添加参数--tag=CXX或--tag=CC

##### 处理
<pre>
LTOBJCCOMPILE = $(LIBTOOL) $(AM_V_lt) <font color="ff0000"> --tag=CC </font>$(AM_LIBTOOLFLAGS) \ 
...
OBJCLINK = $(LIBTOOL) $(AM_V_lt) <font color="ff0000"> --tag=CC </font> $(AM_LIBTOOLFLAGS) $(LIBTOOLFLAGS)
...
</pre>

### 12. /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/usr/bin/strings: No such file or directory
<pre>
Selecting SDK path = /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator8.2.sdk
./configure: line 730: /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/usr/bin/strings: No such file or directory
./configure: line 732: /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/usr/bin/strings: No such file or directory
endian test failed
builders.d/x264.mk:53: recipe for target '/Users/starnet/Projects/linphone-iphone/submodules/build/../build-i386-apple-darwin/externals/x264/config.mak' failed
</pre>
解决：
建立软连接
<pre>
sudo ln -s /Applications/Xcode.app/Contents/Developer//Toolchains/XcodeDefault.xctoolchain/usr/bin/strings /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/usr/bin/
</pre>
### 13.ld: illegal text-relocation to '_x264_cabac_range_lps'
问题
<pre>
ld: illegal text-relocation to '_x264_cabac_range_lps' in libx264.a(cabac.o) from '_x264_cabac_encode_decision_asm' in libx264.a(cabac-a.o) for architecture i386
</pre>
编辑submodules/externals/x264/configure
<pre>
LDFLAGS="$LDFLAGS -read_only_relocs suppress" 
</pre>

## 运行问题汇总
### 1. 登录时crash
##### 问题
<pre>
belle_sip_object_vptr_t *vptr=obj->vptr; 崩溃
</pre>

##### 分析
调用栈:从下到上
<pre>
belle_sip_object_marshal
sal_address_as_string
sal_op_set_route_address
sal_op_add_route_address
linphone_transfer_routes_to_op
linphone_configure_op
linphone_proxy_config_register
linphone_proxy_config_update
ms_list_for_each
proxy_update
linphone_core_iterate
[LinphoneManager iterate]
</pre>

相关结构体
<pre>
struct _belle_sip_object_vptr{
	belle_sip_type_id_t id;
	const char *type_name;
	int initially_unowned;
	belle_sip_object_get_vptr_t get_parent;
	struct belle_sip_interface_desc **interfaces; /*NULL terminated table of */
	belle_sip_object_destroy_t destroy;
	belle_sip_object_clone_t clone;
	belle_sip_object_marshal_t marshal;
	int tostring_bufsize_hint; /*optimization: you can suggest here the typical size for a to_string() result.*/
};

struct _belle_sip_object{
	belle_sip_object_vptr_t *vptr;
	size_t size;
	int ref;
	char* name;
	struct weak_ref *weak_refs;
	struct belle_sip_object_pool *pool;
	struct _belle_sip_list *pool_iterator;
	struct _belle_sip_list *data_store;
};

</pre>

通过分析发现是由于sal_address_destroy释放一个空指针，应该是linphone的bug，目前通过如下方式解决:
修改submodules/linphone/coreapi/bellesip_sal/sal_address_impl.c 
<pre>
void sal_address_destroy(SalAddress *addr){
    if (addr) sal_address_unref(addr);
}
</pre>



### 2. ortp-warning-There is no object pool created in thread [43003904]. Use belle_sip_object_pool_push() to create one. Unowned objects not unref'd will be leaked.

定位在belle-sip/belle_sip_object.c -> get_current_pool_stack -》 belle_sip_thread_getspecific

belle_sip_thread_getspecific在传入相同值，返回的结果有时会不一样，部分情况返回NULL，于是导致后面的代码出错，目前暂未找到根本原因，暂时对后面crash的地方进行参数判断.

* belle_sip_header_address_get_uri
<pre>
belle_sip_uri_t* belle_sip_header_address_get_uri(const belle_sip_header_address_t* address) {
    return address ? address->uri : NULL;//此处添加判断
}
</pre>
* sal_address_impl.c -> sal_address_as_string_uri_only
<pre>
char *sal_address_as_string_uri_only(const SalAddress *addr){
	belle_sip_header_address_t* header_addr = BELLE_SIP_HEADER_ADDRESS(addr);
	belle_sip_uri_t* uri = belle_sip_header_address_get_uri(header_addr);
    if (!uri) return NULL;//此次添加判断
    
	char tmp[1024]={0};
	size_t off=0;
	belle_sip_object_marshal((belle_sip_object_t*)uri,tmp,sizeof(tmp),&off);
	return ms_strdup(tmp);
}
</pre>
 
此问题已解决，详情猛戳[这里](http://wenva.github.io/ios/2015/04/08/%E7%BA%BF%E7%A8%8B%E5%B1%80%E9%83%A8%E5%AD%98%E5%82%A8.html)