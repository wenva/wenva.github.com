---
layout: post
title: "树莓派1 B+ OSMC支持HiFiBerry"
date: 2015-11-12
comments: false
categories: 树莓派
---

最新版本的OSMC已经完美地支持了HiFiBerry，大家只要进行相关设置就ok，不用aplay、/etc/modules各种折腾（我就这么过来的）

### 配置

* 开启HiFiBerry声卡

<pre>
My OSMC -> Pi Config -> Hardware Support -> Soundcard Overlay
选择 hifiberry-dacplus-overlay
</pre>
PS: 这里我是DAC+，因此是hifiberry-dacplus-overlay，还有DAC、DIGI、APM+等各硬件扩展，请自行选择

* 去掉LIRC

<pre>
My OSMC -> Pi Config -> Hardware Support -> Enable LIRC GPIO support
设置NO
</pre>

![image](http://7ximmr.com1.z0.glb.clouddn.com/osmc-hifiberry.jpg)

* 设置声音输出为HiFiBerry

<pre>
Settings -> System -> Audio Output -> Audio output device
设置为:ALSA: Default(snd_rpi_hifiberry_dacplus Analog)
</pre>

![image](http://7ximmr.com1.z0.glb.clouddn.com/osmc-audio-ouput-hifiberry.jpg)
