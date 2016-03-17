---
layout: post
title: "linphone源码解读之Filter"
date: 2016-03-17
comments: false
categories: iOS
---

Filter是linphone源码的精髓，Filter可以比作过滤器，负责对数据进行不同功能的操作，如解码、编码、显示、滤噪等等. 往往一个流程需要很多歌Filter来组成，只有经过一层层的过滤，才能得到纯净的数据. 比如视频接收显示流程，需要经过rtprecv、decoder、tee、jpegwriter、display几个Filter. 下面我们来详细地讲述Filter.

### 定义
<pre>
struct _MSFilterDesc{
	MSFilterId id;
	const char *name;
	const char *text;
	MSFilterCategory category;
	const char *enc_fmt;
	int ninputs;
	int noutputs;
	MSFilterFunc init;
	MSFilterFunc preprocess;
	MSFilterFunc process;
	MSFilterFunc postprocess;
	MSFilterFunc uninit;
	MSFilterMethod *methods;
	unsigned int flags;
};

struct _MSFilter{
	MSFilterDesc *desc; //描述，指定过滤id、名称、函数指针（初始化、预处理、处理、反初始化）
	ms_mutex_t lock;
	MSQueue **inputs; //输入源
	MSQueue **outputs; //输出源
	struct _MSFactory *factory;
	void *padding;
	void *data;
	struct _MSTicker *ticker;
	MSList *notify_callbacks;
	uint32_t last_tick;
	MSFilterStats *stats;
	int postponed_task;
	bool_t seen;
};
</pre>
PS: 每种类型的Filter仅有一个Desc，该Desc定于实现文件中，并通过EXPORT来引用.

### 创建
创建一个Filter的方式比较多，可以根据id、name、desc等等，如下是五种创建方式，足够用.
<pre>
MS2_PUBLIC MSFilter * ms_filter_create_encoder(const char *mime); //创建编码Filter
MS2_PUBLIC MSFilter * ms_filter_create_decoder(const char *mime); //创建解码Filter
MS2_PUBLIC MSFilter *ms_filter_new(MSFilterId id); //根据Id创建Filter
MS2_PUBLIC MSFilter *ms_filter_new_from_name(const char *name); //根据名称创建Filter
MS2_PUBLIC MSFilter *ms_filter_new_from_desc(MSFilterDesc *desc); //根据描述创建Filter
</pre>
### 连接
在文章开头我已声明过，一个流程可能会有多个Filter，那么问题来了，我们如何关联这个Filter？这里大家可以想到化学实验课时，我们一般会使用一个导管把上一步的输出接到下一步的输入，这里也一样，我们可以通过ms_filter_link来连接2个Filter.

<pre>
// 连接f1的outputs[pin1]与f2的inputs[pin2]
int ms_filter_link(MSFilter *f1, int pin1, MSFilter *f2, int pin2){
	MSQueue *q; //可以理解为导管
	...
	q=ms_queue_new(f1,pin1,f2,pin2);
	f1->outputs[pin1]=q;
	f2->inputs[pin2]=q;
	return 0;
}
</pre>

### 断开
有连接操作就有断开操作，当需要断开2个Filter又如何操作呢，那就是去掉导管
<pre>
int ms_filter_unlink(MSFilter *f1, int pin1, MSFilter *f2, int pin2){
	MSQueue *q;
	...
	q=f1->outputs[pin1];
	f1->outputs[pin1]=f2->inputs[pin2]=0;
	ms_queue_destroy(q);
	return 0;
}
</pre>

### 销毁
为了保证资源的正确释放，需要调用销毁接口
<pre>
void ms_filter_destroy(MSFilter *f)
</pre>
