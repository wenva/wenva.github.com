---
layout: post
title: "lighttpd支持HTTPS"
date: 2017-04-06
comments: false
categories: BACK-END
---

随着Apple、Google大力推广HTTPS，HTTPS将成为今后网站的主流，而前段时间正好看到[Let’s Encrypt](https://letsencrypt.org/)可以生成免费的SSL证书。因此尝试配置了下lighttpd，发现非常容易，大体步骤如下:

## 申请证书

#### 1. 获取Certbot

```
git clone https://github.com/certbot/certbot
```

#### 2. 申请证书

```
cd certbot
./letsencrypt-auto certonly -d smallmuou.xyz
```
PS: 选择Automatically use a temporary webserver(stadalone)

#### 3. 配置证书
成功后，会生成如下几个文件

```
smallmuou:~ $ tree /etc/letsencrypt/live/smallmuou.xyz/
/etc/letsencrypt/live/smallmuou.xyz/
|-- cert.pem -> ../../archive/smallmuou.xyz/cert1.pem
|-- chain.pem -> ../../archive/smallmuou.xyz/chain1.pem
|-- fullchain.pem -> ../../archive/smallmuou.xyz/fullchain1.pem
|-- privkey.pem -> ../../archive/smallmuou.xyz/privkey1.pem
|-- README
```
PS: 各个文件的含义可以查看README的说明，我也给出我的理解

* cert.pem 公钥
* prikey.pem 私钥
* fullchain.pem CA证书信任链 (包含Root Certificate)
* chain.pem 上一级CA证书（这里指Let's Encrypt）

PS: 可以通过`cat cert.pem prikey.pem > server.pem`将私有和公用打包在一起，以供后续lighttpd配置使用.

信任链（chain）即证书的信任关系，如A信任A1，A1信任A2，其中最顶级的节点就是根证书（root certificate），Let’s Encrypt就是直接隶属于root certificate. 

```
└── DST Root CA X3
    └── Let's Encrypt Authority X3
        └── smallmuou.xyz
```

## 安装及配置lighttpd

#### 1. [安装SSL](https://redmine.lighttpd.net/projects/1/wiki/docs_ssl#How-to-install-SSL)

```
yum install openssl*
```

#### 2. 下载

进入[lighttpd官网](http://www.lighttpd.net/)，下载lighttpd源码包

```
wget http://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.45.tar.gz
```

#### 3. 解压并编译

```
tar xzvf lighttpd-1.4.45.tar.gz
cd lighttpd-1.4.45
./autogen.sh
./configure --with-openssl --with-openssl-libs=/usr/lib
make 
make install
```
PS: 安装完后，执行`lighttpd -v`，当有出现(ssl)字样，则表示lighttpd已支持SSL

#### 4. 配置
进入`doc/config`编辑lighttpd.conf文件，添加如下内容

```
$SERVER["socket"] == "0.0.0.0:443" {
  ssl.engine                  = "enable"
  ssl.pemfile                 = "/etc/letsencrypt/live/smallmuou.xyz/server.pem"
  ssl.ca-file                 = "/etc/letsencrypt/live/smallmuou.xyz/fullchain.pem"
  server.document-root        = "/srv/www/htdocs"
}

```
* ssl.engine 是否开启SSL
* ssl.pemfile pem文件位置（包含私有和公用）
* ssl.ca-file CA证书
* server.document-root 根路径
点击[此处](https://redmine.lighttpd.net/projects/1/wiki/docs_ssl#How-to-install-SSL)查看更多选项内容

#### 5. 完成

经过以上步骤，重新启动`lighttpd -f lighttpd.conf`，就可以使用https访问，而且是受信任的. 亲测有效.

