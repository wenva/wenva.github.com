---
layout: post
title: "linphone-iphone代码解读"
date: 2015-02-05
comments: false
---
# linphone-iphone代码解读
February 5, 2015

## [流程](http://fossies.org/dox/linphone-3.7.0)
### 1. 初始化startLibLinphone
* （1）模块初始化，包含mediastreamer2、ilbc、silk、amr、x264、h264、bcg729
	<pre>
	ms_init();
	libmsilbc_init();
    libmssilk_init(); 
    libmsamr_init();
	libmsx264_init();
	libmsopenh264_init();
	libmsbcg729_init();
</pre>
* （2）创建linphone core(createLinphoneCore)
	<pre>
	theLinphoneCore = linphone_core_new_with_config (&linphonec_vtable
								 ,configDb
								 ,self /* user_data */);
</pre>
	linphonec_vtable为所有回调接口(见LinphoneManager.m)
	<pre>
	static LinphoneCoreVTable linphonec_vtable = {
	.show =NULL,
	.call_state_changed =(LinphoneCoreCallStateChangedCb)linphone_iphone_call_state,
	.registration_state_changed = linphone_iphone_registration_state,
	.notify_presence_received=NULL,
	.new_subscription_requested = NULL,
	.auth_info_requested = NULL,
	.display_status = linphone_iphone_display_status,
	.display_message=linphone_iphone_log,
	.display_warning=linphone_iphone_log,
	.display_url=NULL,
	.text_received=NULL,
	.message_received=linphone_iphone_message_received,
	.dtmf_received=NULL,
    .transfer_state_changed=linphone_iphone_transfer_state_changed,
    .is_composing_received = linphone_iphone_is_composing_received,
    .configuring_status = linphone_iphone_configuring_status_changed,
    .global_state_changed = linphone_iphone_global_state_changed
	};
</pre>
	LinphoneCoreVTable包含:
	* global_state_changed 全局状态改变回调
	* registration_state_changed 注册状态改变回调
	* call_state_changed 呼叫状态改变回调
	* ...(详见linphonecore.h)
	
* （3）初始化audio session
	<pre>
	AVAudioSession *audioSession = [AVAudioSession sharedInstance]	;
	BOOL bAudioInputAvailable= audioSession.inputAvailable	;
	[audioSession setActive:NO error: &err	]
</pre>

### 2. 注册
* （1）linphone_auth_info_new 生成认证信息
* （2）linphone_core_clear_all_auth_info 清空所有认证信息
* （3）linphone_core_add_auth_info添加认证信息

### 3. 配置项
配置项采用InAppSettings第三方库来实现的，存储于InAppSettings.bundle中得plist文件下，在LinphoneManager初始化会通过migrateFromUserPrefs来同步一次配置项；
在退出设置界面时会调用[LinphoneCoreSettingsStore synchronize]来生效配置，如下是一些常用的配置接口:
	<pre>
	linphone_core_set_sip_transports 设置sip传输协议有TCP、UDP、TLS
	linphone_address_set_username 设置用户名
	linphone_address_set_domain 设置域名
	linphone_auth_info_new 创建认证信息，包含用户名、密码、域名
	linphone_core_add_auth_info 添加认证信息
	linphone_core_enable_payload_type 音视频开关配置
</pre>

### 4. 来电
当有来电时，会触发call_state_changed发生变化（linphonec_vtable），于是会调用回调linphone_iphone_call_state
	<pre>
	static void linphone_iphone_call_state(LinphoneCore *lc, LinphoneCall* call, LinphoneCallState state,const char* message) {
	[(LinphoneManager*)linphone_core_get_user_data(lc) onCall:call StateChanged: state withMessage:  message];
}
</pre>
呼叫状态值如下:
	<pre>
	typedef enum _LinphoneCallState{
	LinphoneCallIdle = 0, //初始化状态
	LinphoneCallIncomingReceived = 1, //来电
	LinphoneCallOutgoingInit = 2, //开始呼出
	LinphoneCallOutgoingProgress = 3, //正在处理呼出
	LinphoneCallOutgoingRinging = 4, //呼出正在响铃
	LinphoneCallOutgoingEarlyMedia = 5,
	LinphoneCallConnected = 6, //接通
	LinphoneCallStreamsRunning = 7, //媒体流通道构建成功
	LinphoneCallPausing = 8, 
	LinphoneCallPaused = 9,
	LinphoneCallResuming = 10,
	LinphoneCallRefered = 11,//有新来电，转出当前回话
	LinphoneCallError = 12,
	LinphoneCallEnd = 13, //结束
	LinphoneCallPausedByRemote = 14, //远程结束
	LinphoneCallUpdatedByRemote = 15, //配置更新，如视频开启
	LinphoneCallIncomingEarlyMedia = 16,
	LinphoneCallUpdating = 17,
	LinphoneCallReleased = 18
} LinphoneCallState;
</pre>

### 5. 接听
* 弹出IncomingCallViewController
	<pre>
linphone_iphone_call_state -> [LinphoneManager onCall:StateChanged:withMessage] -> [PhoneMainView callUpdate]->[PhoneMainView displayIncomingCall] -> IncomingCallViewController
</pre>

* 点击接听
	<pre>
	onAcceptClick -> [PhoneMainView incomingCallAccepted] -> acceptCall->linphone_core_accept_call_with_params
</pre>
	
### 6. 呼出
* 呼出
	<pre>
	DialerViewController ->[UICallButton touchUp:]-> [LinphoneManager call:displayName:transfer:] -> linphone_core_invite_address_with_params
	</pre>

### 7. 摄像头设备
* 前置后置
	<pre>
	linphone_core_get_video_devices 获取所有设备号
	linphone_core_set_video_device 设置设备号
	linphone_core_get_video_device 获取当前设备号
</pre>

### 8. 摄像头视频显示
* 设置view
	<pre>
	linphone_core_set_native_preview_window_id(lc, view);
</pre>

* mediastreamer2/src/videofilters/ioscapture.m
	<pre>
 	MSFilterDesc ms_ioscapture_desc = {
 	.id=MS_V4L_ID,
  	.name="MSioscapture",
  	.text="A video for IOS compatible source filter to stream pictures.",
  	.ninputs=0,
    .noutputs=1,
    .category=MS_FILTER_OTHER,
    .init=ioscapture_init,
    .preprocess=ioscapture_preprocess,
    .process=ioscapture_process,
    .postprocess=ioscapture_postprocess,
    .uninit=ioscapture_uninit,
    .methods=methods
    }; 
</pre>
	startLibLinphone -> ms_init -> ms_voip_init -> ms_factory_init_voip -> ms_web_cam_manager_register_desc -> ms_v4ios_cam_desc.detect -> ms_v4ios_detect
	<pre>
	
</pre>