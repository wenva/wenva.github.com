---
layout: post
title: "asterisk配置mysql来保存peers"
date: 2017-09-07
comments: false
categories: sip
---

asterisk是一个开源的sip服务器，默认情况，asterisk是从sip.conf来配置peers，如果peers有变更或者数量比较大，就不能采用这种方式，asterisk提供的realtime方式，支持数据库保存peers，有包括mysql、sqlite、postgres等，本文将指导如何进行mysql配置.

### 步骤1 - 安装并配置mysql

可以参考其他文档安装mysql，并配置用户密码

### 步骤2 - 创建数据库及表

```sql
CREATE DATABASE asterisk;
CREATE TABLE IF NOT EXISTS `sippeers` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(10) NOT NULL,
      `ipaddr` varchar(15) DEFAULT NULL,
      `port` int(5) DEFAULT NULL,
      `regseconds` int(11) DEFAULT NULL,
      `defaultuser` varchar(10) DEFAULT NULL,
      `fullcontact` varchar(64) DEFAULT NULL,
      `regserver` varchar(20) DEFAULT NULL,
      `useragent` varchar(64) DEFAULT NULL,
      `lastms` int(11) DEFAULT NULL,
      `host` varchar(40) DEFAULT NULL,
      `type` enum('friend','user','peer') DEFAULT NULL,
      `context` varchar(40) DEFAULT NULL,
      `permit` varchar(40) DEFAULT NULL,
      `deny` varchar(40) DEFAULT NULL,
      `secret` varchar(40) DEFAULT NULL,
      `md5secret` varchar(40) DEFAULT NULL,
      `remotesecret` varchar(40) DEFAULT NULL,
      `transport` enum('udp','tcp','udp,tcp','tcp,udp') DEFAULT NULL,
      `dtmfmode` enum('rfc2833','info','shortinfo','inband','auto') DEFAULT NULL,
      `directmedia` enum('yes','no','nonat','update') DEFAULT NULL,
      `nat` enum('yes','no','never','route') DEFAULT NULL,
      `callgroup` varchar(40) DEFAULT NULL,
      `pickupgroup` varchar(40) DEFAULT NULL,
      `language` varchar(40) DEFAULT NULL,
      `allow` varchar(40) DEFAULT NULL,
      `disallow` varchar(40) DEFAULT NULL,
      `insecure` varchar(40) DEFAULT NULL,
      `trustrpid` enum('yes','no') DEFAULT NULL,
      `progressinband` enum('yes','no','never') DEFAULT NULL,
      `promiscredir` enum('yes','no') DEFAULT NULL,
      `useclientcode` enum('yes','no') DEFAULT NULL,
      `accountcode` varchar(40) DEFAULT NULL,
      `setvar` varchar(40) DEFAULT NULL,
      `callerid` varchar(40) DEFAULT NULL,
      `amaflags` varchar(40) DEFAULT NULL,
      `callcounter` enum('yes','no') DEFAULT NULL,
      `busylevel` int(11) DEFAULT NULL,
      `allowoverlap` enum('yes','no') DEFAULT NULL,
      `allowsubscribe` enum('yes','no') DEFAULT NULL,
      `videosupport` enum('yes','no') DEFAULT NULL,
      `maxcallbitrate` int(11) DEFAULT NULL,
      `rfc2833compensate` enum('yes','no') DEFAULT NULL,
      `mailbox` varchar(40) DEFAULT NULL,
      `session-timers` enum('accept','refuse','originate') DEFAULT NULL,
      `session-expires` int(11) DEFAULT NULL,
      `session-minse` int(11) DEFAULT NULL,
      `session-refresher` enum('uac','uas') DEFAULT NULL,
      `t38pt_usertpsource` varchar(40) DEFAULT NULL,
      `regexten` varchar(40) DEFAULT NULL,
      `fromdomain` varchar(40) DEFAULT NULL,
      `fromuser` varchar(40) DEFAULT NULL,
      `qualify` varchar(40) DEFAULT NULL,
      `defaultip` varchar(40) DEFAULT NULL,
      `rtptimeout` int(11) DEFAULT NULL,
      `rtpholdtimeout` int(11) DEFAULT NULL,
      `sendrpid` enum('yes','no') DEFAULT NULL,
      `outboundproxy` varchar(40) DEFAULT NULL,
      `callbackextension` varchar(40) DEFAULT NULL,
      `registertrying` enum('yes','no') DEFAULT NULL,
      `timert1` int(11) DEFAULT NULL,
      `timerb` int(11) DEFAULT NULL,
      `qualifyfreq` int(11) DEFAULT NULL,
      `constantssrc` enum('yes','no') DEFAULT NULL,
      `contactpermit` varchar(40) DEFAULT NULL,
      `contactdeny` varchar(40) DEFAULT NULL,
      `usereqphone` enum('yes','no') DEFAULT NULL,
      `textsupport` enum('yes','no') DEFAULT NULL,
      `faxdetect` enum('yes','no') DEFAULT NULL,
      `buggymwi` enum('yes','no') DEFAULT NULL,
      `auth` varchar(40) DEFAULT NULL,
      `fullname` varchar(40) DEFAULT NULL,
      `trunkname` varchar(40) DEFAULT NULL,
      `cid_number` varchar(40) DEFAULT NULL,
      `callingpres` enum('allowed_not_screened','allowed_passed_screen','allowed_failed_screen','allowed','prohib_not_screened','prohib_passed_screen','prohib_failed_screen','prohib') DEFAULT NULL,
      `mohinterpret` varchar(40) DEFAULT NULL,
      `mohsuggest` varchar(40) DEFAULT NULL,
      `parkinglot` varchar(40) DEFAULT NULL,
      `hasvoicemail` enum('yes','no') DEFAULT NULL,
      `subscribemwi` enum('yes','no') DEFAULT NULL,
      `vmexten` varchar(40) DEFAULT NULL,
      `autoframing` enum('yes','no') DEFAULT NULL,
      `rtpkeepalive` int(11) DEFAULT NULL,
      `call-limit` int(11) DEFAULT NULL,
      `g726nonstandard` enum('yes','no') DEFAULT NULL,
      `ignoresdpversion` enum('yes','no') DEFAULT NULL,
      `allowtransfer` enum('yes','no') DEFAULT NULL,
      `dynamic` enum('yes','no') DEFAULT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `name` (`name`),
      KEY `ipaddr` (`ipaddr`,`port`),
      KEY `host` (`host`,`port`)
) ENGINE=MyISAM;
```

### 步骤3 - 编译asterisk的mysql模块

```bash
make menuconfig
```
勾选 addons->res_config_mysql，并重新make && make install

### 步骤4 - 配置res_config_mysql.conf

```
[general]
dbhost = 127.0.0.1
dbname = asterisk
dbuser = root
dbpass = 123456
dbport = 3306
dbsock = /var/lib/mysql/mysql.sock
dbcharset = utf8
```
PS: dbname数据库名字， dbsock为mysql的本地sock文件，需要根据自己环境变更


### 步骤5 - 配置extconfig.conf

vim /etc/asterisk/extconfig.conf
```
sippeers => mysql,general,sippeers
```
PS: general是对应res_config_mysql.conf的段名（中括号部分）， sippeers为数据库表名

### 步骤6 - 插入用户信息

```sql
INSERT INTO sippeers (name, host, secret) values ('111', 'dynamic', '111');
```
PS: name用户名，secret密码，host必须指定为dynamic，否则注册不了

### 步骤7 - 启动asterisk

```bash
asterisk
```
此时就可以正常注册了，如果提示插入失败，请查看asterisk控制台的报错信息，一般是长度超出了mysql表定义的字段长度。

以上是我配置的整个过程，当然中间踩了很多坑，不过都可以通过asterisk控制台看出.