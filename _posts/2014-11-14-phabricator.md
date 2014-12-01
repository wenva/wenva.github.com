---
layout: post
title: "Phabricator"
date: 2014-11-14
comments: false
---
# Phabricator


### Install


### Config

#### 配置帐号和注册（Configuring Accounts and Registration）
* 当administrator帐号进不去，则可以通过./bin/auth recover <username>恢复
* ./bin/accountadmin 添加用户

### Differential(Pre-Review)-提交前审查
* 创建分支 git checkout -b <new branch>
* 编辑修改代码
* arc diff,填写修改内容
* Reviewer 进入 Differential界面审查代码
* Accept后，arc land <new branch>

### Audit(Post-Review)-提交后审查
* 当提交的commit信息中末尾添加：换行+Auditors:xxx，就可以自动生成Audit Request.
* 与Differential比较，具有如下优势:
	* 不用安装第三方工具
	* 不用等待