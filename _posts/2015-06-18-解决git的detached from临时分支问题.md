---
layout: post
title: "解决git的detached from临时分支问题"
date: 2015-06-18
comments: false
categories: 技巧
---

今天偶然发现git会出现detached from的分支, 导致很多commit未push到服务器，以至于其他同事clone的代码编译错误
<pre>
StarnetdeMacBook-Pro:mediastreamer2 starnet$ git branch -a
* (detached from b34a935)
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
</pre>
google发现如下解决方案

### 解决方案
<pre>
$ git branch temp e9abc7a
$ git checkout temp
Switched to branch 'temp'
$ git branch
  master
* temp
$ git log --graph --decorate --pretty=oneline --abbrev-commit master origin/master temp
* e9abc7a (HEAD, temp) push release notes 1.16 (again)
* 2f5d3fd adding the release notes for 1.16 to doc/
* 4581e52 (tag: rear-1.16, origin/master, origin/HEAD, master) prepare rear for new release 1.16
*   de337d4 Merge pull request #403 from ypid/df-encfs-fix

$ git diff master temp
diff --git a/doc/rear-release-notes.txt b/doc/rear-release-notes.txt
....

$ git diff origin/master temp
diff --git a/doc/rear-release-notes.txt b/doc/rear-release-notes.txt
....
$ git branch -f master temp
$ git checkout master
Switched to branch 'master'
Your branch is ahead of 'origin/master' by 2 commits.
  (use "git push" to publish your local commits)
$ git push
$ git branch -d temp
Deleted branch temp (was e9abc7a).
</pre>