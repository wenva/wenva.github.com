---
layout: post
title: "创建自己的CocoaPods私有仓库"
date: 2015-07-08
comments: false
categories: 
---
引入CocoaPods来管理iOS第三方库有一段时间了，这里说一下体会 "快乐并痛着"，为何说快乐呢，可以方便我们去寻找第三方库，并引入到已有的项目工程中，而且保证了工程结构的清晰；为何又说痛着呢，主要是由于更新第三方库太慢了，目前我们引用的第三方库已将近20个，更新一次耗费了至少得半个小时以上，而且更可恶的是，更新期间无法编译代码；总的来说，还是痛多些，现在都不敢更新，于是Google下，发现[CocoaPods支持私有仓库](https://guides.cocoapods.org/making/private-cocoapods.html). 这里简单描述我的经过.

### 1. 创建Repo
<pre>
StarnetdeMacBook-Pro:EVideoSpecs starnet$ tree
.
├── CocoaPods-version.yml
├── README.md
└── Specs
    ├── AAPullToRefresh
    │   └── 1.0.2
    │       └── AAPullToRefresh.podspec.json
    ├── PPAdvertisingView
    │   └── 1.0.0
    │       └── PPAdvertisingView.podspec
    └── SDWebImage
        └── 3.7.2
            └── SDWebImage.podspec

7 directories, 5 files

</pre>
Repo结构如上，大致说明下

* CocoaPods-version.yml - CocoaPods版本信息，可以到CocoaPods的官方[Repo](https://github.com/CocoaPods/Specs)拷贝
* Specs - 存放第三方库的.podspec，可以先为空，后续再添加

创建好后，提交到自己的Git服务器上，比如我的: http://192.168.61.223/xuwf/evideospecs.git

### 2. 添加到CocoaPods
<pre>
pod repo add EVideoSpecs http://192.168.61.223/xuwf/evideospecs.git
</pre>
不懂，查帮助`pod repo help`

### 3. 添加第三方库podspec文件
<pre>
├── Specs
    └── [SPEC_NAME]
        └── [VERSION]
            └── [SPEC_NAME].podspec

</pre>
可以自己创建podspec，也可以直接去CocoaPods的官方[Repo](https://github.com/CocoaPods/Specs)拷贝，比如我拷贝了AAPullToRefresh.podspec.json

可以用` pod spec lint`验证.podspec合法性，这里说明一点，从CocoaPods的官方Repo看到的都是json格式，这里可以通过`pod ipc spec`来将spec文件转换成json.

### 4. 更新Repo
<pre>
git add .
git commit -m "添加了AAPullToRefresh第三方库"
git push origin master
</pre>
更新CocoaPods的Repo
<pre>
pod repo update
</pre>

### 5. 验证
此时通过`pod search 您的库名`就能检索出你添加的第三方库

### 6. 添加到工程
编辑Podfile
<pre>
source 您的私有Repo地址  # 我的: source 'http://192.168.61.223/xuwf/evideospecs'

pod '您的第三方库'
</pre>
重点说明下，必须添加source，否则`pod install`会默认去Clone CocoaPods的官方Repo到本地，这得卡好久好久，因此强烈建议加上

### 7. pod install/update
后续的操作，大家应该都比较清晰，这里不做阐述.