---
layout: post
title: "font-awesome 字体文件路径如何配置"
date: 2016-12-08
comments: false
categories: FRONT-END
---

最近工程中有使用到font-awesome，其中涉及到font路径的配置纠结了我好长一段时间，经过探索发现，该路径是相对于css路径.

### css模式

当直接使用css模式，则从官网下载后的目录结构是：(3.2.1)
<pre>
starnet:Font-Awesome-3.2.1 $ tree .
.
├── css
│   ├── font-awesome-ie7.css
│   ├── font-awesome-ie7.min.css
│   ├── font-awesome.css
│   └── font-awesome.min.css
├── font
│   ├── FontAwesome.otf
│   ├── fontawesome-webfont.eot
│   ├── fontawesome-webfont.svg
│   ├── fontawesome-webfont.ttf
│   └── fontawesome-webfont.woff
└── scss
    ├── _bootstrap.scss
    ├── _core.scss
    ├── _extras.scss
    ├── _icons.scss
    ├── _mixins.scss
    ├── _path.scss
    ├── _variables.scss
    ├── font-awesome-ie7.scss
    └── font-awesome.scss
</pre>
PS: 此处只列出相关文件，其他文件不列出

打开font-awesome.css可以看到如下信息：

<pre>
@font-face {
  font-family: 'FontAwesome';
  src: url('../font/fontawesome-webfont.eot?v=3.2.1');
  src: url('../font/fontawesome-webfont.eot?#iefix&v=3.2.1') format('embedded-opentype'), url('../font/fontawesome-webfont.woff?v=3.2.1') format('woff'), url('../font/fontawesome-webfont.ttf?v=3.2.1') format('truetype'), url('../font/fontawesome-webfont.svg#fontawesomeregular?v=3.2.1') format('svg');
  font-weight: normal;
  font-style: normal;
}
</pre>
PS: ../font/fontawesome-webfont.eot?v=3.2.1路径是以css文件所在位置为当前位置

### sass模式
sass是中间文件，通过import后，sass文件会合并成一个，因此生成的css可能就不是font-awesome.css，因此路径也就不是`../font`，有两种做法：

* 方法一：修改路径配置
vim _variables.scss

<pre>
$fa-font-path:        "../font" !default;
</pre>

* 方法二：拷贝字体

<pre>
cp font css文件上一级
</pre>

