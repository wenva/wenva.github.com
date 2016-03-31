---
layout: post
title: "linphone源码解读之Filter"
date: 2016-03-17
comments: false
categories: iOS
---

Filter是linphone源码的精髓，Filter可以比作过滤器，负责对数据进行不同功能的操作，如解码、编码、显示、滤噪等等. 往往一个流程需要很多个Filter来组成，只有经过一层层的过滤，才能得到【纯净】的数据. 比如视频接收显示流程，需要经过rtprecv、decoder、tee、jpegwriter、display几个Filter. 下面我们来详细地讲述Filter.

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

在文章开头我已声明过，一个流程可能会有多个Filter，那么问题来了，我们如何关联这些Filter？这里大家可以想到化学实验课时，我们一般会使用一个导管把上一步的输出接到下一步的输入，这里也一样，我们可以通过ms_filter_link来连接2个Filter.

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


### 实例 - 视频接收显示

#### 启动视频

videostream.c
<pre>
int video_stream_start_with_source (VideoStream *stream, RtpProfile *profile, const char *rem_rtp_ip, int rem_rtp_port,
	const char *rem_rtcp_ip, int rem_rtcp_port, int payload, int jitt_comp, MSWebCam* cam, MSFilter* source, bool_t discard_decode_error){
		...
		/* 创建 */
		stream->ms.decoder=ms_filter_create_decoder(pt->mime_type);
		if (stream->ms.decoder==NULL){
			/* big problem: we don't have a registered decoderfor this payload...*/
			ms_error("videostream.c: No decoder available for payload %i:%s.",payload,pt->mime_type);
			return -1;
		}
		...
		/* display logic */
		stream->output = ms_filter_new_from_name (stream->display_name);
		stream->ms.rtprecv = ms_filter_new (MS_RTP_RECV_ID);
		ms_filter_call_method(stream->ms.rtprecv,MS_RTP_RECV_SET_SESSION,stream->ms.sessions.rtp_session);

		if (stream->output_performs_decoding == FALSE) {
			stream->jpegwriter=ms_filter_new(MS_JPEG_WRITER_ID);
			if (stream->jpegwriter){
				stream->tee2=ms_filter_new(MS_TEE_ID);
			}
		}
		...
		/* 连接 */
		ms_connection_helper_start (&ch);
		ms_connection_helper_link (&ch,stream->ms.rtprecv,-1,0);
		if (stream->output_performs_decoding == FALSE) {
			if (stream->itcsink){
				ms_connection_helper_link(&ch,stream->tee3,0,0);
				ms_filter_link(stream->tee3,1,stream->itcsink,0);
				configure_itc(stream);
			}
			ms_connection_helper_link(&ch,stream->ms.decoder,0,0);
		}
		if (stream->tee2){
			ms_connection_helper_link (&ch,stream->tee2,0,0);
			ms_filter_link(stream->tee2,1,stream->jpegwriter,0);
		}
		if (stream->output!=NULL)
			ms_connection_helper_link (&ch,stream->output,0,-1);
		...
}
</pre>
PS: tee是一分多过滤器，一个输入多个输出
可以看出视频输出经过的过滤器依次是：ms.rtprecv -》 ms.decoder -》 tee2 -》jpegwriter-》output

ms_connection_helper_link可以理解队列，filter依次加到其尾部

#### 停止视频
videostream.c
<pre>
void
video_stream_stop (VideoStream * stream)
{
...
			} else if (stream->ms.rtprecv){
				MSConnectionHelper h;
				ms_connection_helper_start (&h);
				ms_connection_helper_unlink (&h,stream->ms.rtprecv,-1,0);
				if (stream->output_performs_decoding == FALSE) {
					if (stream->itcsink){
						ms_connection_helper_unlink(&h,stream->tee3,0,0);
						ms_filter_unlink(stream->tee3,1,stream->itcsink,0);
					}
					ms_connection_helper_unlink (&h,stream->ms.decoder,0,0);
				}
				if (stream->tee2){
					ms_connection_helper_unlink (&h,stream->tee2,0,0);
					ms_filter_unlink(stream->tee2,1,stream->jpegwriter,0);
				}
				if(stream->output)
					ms_connection_helper_unlink (&h,stream->output,0,-1);
				if (stream->tee && stream->output && stream->output2==NULL)
					ms_filter_unlink(stream->tee,1,stream->output,1);
			}
		}
	}
...
}
</pre>