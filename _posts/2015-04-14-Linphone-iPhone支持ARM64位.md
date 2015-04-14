---
layout: post
title: "Linphone-iPhone支持ARM64位"
date: 2015-04-14
comments: false
categories: iOS
---
Linphone-iOS 2.2.4以前是不支持arm64，而去下载官网的源码又很耗时间，于是自己尝试添加ARM64的支持，现在我将具体的过程记录于此，方便自己后期查看，也希望能为爱自己折腾的人提供帮助.

### 添加ARM64
* 修改submodules/build/Makefile，添加ARM64支持
<pre>
arm64-%:
	make -f builder-iphone-os.mk host=arm-apple-darwin $(LINPHONE_OPTIONS) $*

...

build-% clean-% veryclean-%: 
	make -f builder-iphone-simulator.mk $(LINPHONE_OPTIONS) $@ \
	&& make -f builder-iphone-os.mk $(LINPHONE_OPTIONS) $@ \
	&& make -f builder-iphone-os.mk host=armv7s-apple-darwin $(LINPHONE_OPTIONS) $@ \
	&& make -f builder-iphone-os.mk host=armv-apple-darwin $(LINPHONE_OPTIONS) $@

# sends the target after 'broadcast_' to all sub-architectures (armv7, armv7s, arm64, simulator)
broadcast_%:
	@echo "Broadcasting target '$*' to all sub-architectures"
	make -f builder-iphone-simulator.mk $(LINPHONE_OPTIONS) $* \
	&& make -f builder-iphone-os.mk $(LINPHONE_OPTIONS) $* \
	&& make -f builder-iphone-os.mk host=armv7s-apple-darwin $(LINPHONE_OPTIONS) $* \
	&& make -f builder-iphone-os.mk host=arm-apple-darwin $(LINPHONE_OPTIONS) $*
</pre>
* 编辑submodules/build/builder-iphone-os.mk，添加ARM64编译
<pre>

</pre>


#### 各种坑
* "_CFReadStreamClose", referenced from
<pre>
Undefined symbols for architecture arm64:
  "_CFReadStreamClose", referenced from:
      _stream_channel_close in libbellesip.a(libbellesip_la-stream_channel.o)
  "_CFReadStreamOpen", referenced from:
      _finalize_stream_connection in libbellesip.a(libbellesip_la-stream_channel.o)
  "_CFReadStreamSetProperty", referenced from:
      _finalize_stream_connection in libbellesip.a(libbellesip_la-stream_channel.o)
</pre>
经过分析是由于未添加相应的framework，通过编辑submodules/belle-sip/configure.ac
<pre>
case "$target" in
	*-apple-darwin.ios|i386-apple*|arm-apple|armv6-apple*|armv7-apple*|armv7s-apple*|arm64-apple*|aarch64-apple*)
		LIBS="$LIBS -framework Foundation -framework CoreFoundation -framework CFNetwork -framework UIKit"
		build_apple=yes
	;;	
	#macosx 64 bits
	x86_64-apple-darwin*)
		LIBS="$LIBS -framework Foundation"
		OBJCFLAGS="$OBJCFLAGS  -fmodules"
		build_apple=yes
	;;
esac
</pre>
将arm-apple改为arm-apple*

* error: unrecognized instruction mnemonic
<pre>
/Users/starnet/Projects/linphone-iphone/submodules/build/..//externals/speex/libspeex/fixed_arm5e.h:51:8: error: unrecognized instruction mnemonic
  asm ("smlabb  %0,%1,%2,%3;\n"
 ...
</pre>
