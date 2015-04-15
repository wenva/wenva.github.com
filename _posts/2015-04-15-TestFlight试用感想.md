---
layout: post
title: "TestFlight试用感想"
date: 2015-04-15
comments: false
categories: iOS
---

一提到iOS APP的测试，估计很多iOS开发者（当然也包括我），肯定在心里头暗骂“好坑”，确实对于一个未发布的APP来说，要测试它，根据以往我的经验，只有以下2个途径来安装APP:

* 越狱（好不安全^-^），直接安装ipa
* 加入开发设备白名单（一个开发账号，总共只能加100，我可不舍得，而且加了还不能移除，好坑）

对于第一种来说，变得越来越不现实了，现在发现周边很多同事都不越狱，于是乎总不能为了让他们测试，把他们设备越狱了吧（显然要被揍）；而对于第二种，不是设备名额现在，光操作就很麻烦，获取UUID，添加UUID，重新生成profile，重新编译，重新打包；（赶紧更坑）。前些天听一个同事说，有个TestFilight可以在APP未发布时，就能发邮件邀请其他测试人员。激动是不用说了，果断试了一下，还真是，下面聊聊我的试用感谢.

### TestFlight为何方神圣？
查阅谷歌，了解到TestFlight原先是由Burstly推出的，2014年被苹果大神（Apple）收购了，并在iOS中发布了一个叫做TestFlight的新玩意，用于将Beta测试流水化。TestFlight提供内部测试及外部测试，内部测试最多为25人，外部测试可达1000人，但需要经过苹果审核. 感觉还是内部好，方便，不用经过Apple.

### 怎么用？
* 添加测试员
Web登入iTunes Connect，当然前提是你必须拥有一个Apple Developer Account, 进入"用户职能"，可以看到"iTunes Connect 用户"，"TestFilght Beta版测试员"，“沙箱技术测试员”，进入"iTunes Connect 用户"，点击“+”，添加相应用户

* 测试员会收到相应的激活邮件
激活信类似如下，点击“activate your account”激活
<pre>
iTunes Connect
Welcome to iTunes Connect.
You have successfully created an iTunes Connect account for xuwenfa@star-net.cn.

To complete the process, activate your account using the password already associated with this Apple ID.

If you have any questions about this email, please use Contact Us.

Regards,
The iTunes Store team
</pre>

* 生效测试员
再进入"TestFilght Beta版测试员"，勾选刚添加的用户，添加测试员过程就OVER
* 测试员安装TestFlight（iOS7以下就升级吧，因为苹果最大）
* 预发行APP
进入“我的App”，点击“预发行”，可以看到你用Application Loader上传的应用，点击“内部测试员”，勾选测试员，之后回到“构建版本”，打开“TestFlight Beta 测试”开发.
* 下载应用
测试员会收到测试邀请信，“TestFlight: You're invited to test xxx”，点击“Open in TestFlight”，系统会自动跳转到TestFlight，此时测试者就可以看到相应的APP。（此处当然是用测试者的iOS设备邮箱打开邮件）
![image](https://github.com/wenva/wenva.github.com/raw/master/resource/TestFlight Invite.png)