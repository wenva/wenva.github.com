---
layout: post
title: "linux下nginx反向代理配置"
date: 2017-08-24
comments: false
categories: linux
---

关于反向代理服务器，大家应该都有耳闻，形象地说就是增设的"前台"，所有访问都通过这个前台，不能直接访问内部服务器，从而实现了隐藏. 通过反向代理可以实现重定向、负载均衡等.

#### 1. 安装 pcre

```bash
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.41.tar.gz
./configure
make
make install
```
PS：debain 系可以直接安装 libpcre3-dev

#### 2. 安装 nginx

```bash
wget http://nginx.org/download/nginx-1.13.4.tar.gz
tar xzvf nginx-1.13.4.tar.gz
cd nginx-1.13.4
./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module
make
make install
ln -s /usr/local/nginx/sbin/nginx /usr/local/bin
```

#### 3. 运行nginx

```bash
nginx
```

若遇到找不到 pcre 动态库，则将/usr/local/lib加入系统动态库

```bash
echo '/usr/local/lib' >> /etc/ld.so.conf.d/local.conf
```

#### 4. 添加用户组

```bash
groupadd nginx
useradd -g nginx nginx
```

#### 5. 配置反向代理
vim /usr/local/nginx/conf/nginx.conf

```bash
user nginx nginx;
error_log  logs/error.log;
pid        logs/nginx.pid;
...
http {
    ...
    server {
        server_name localhost;
        ...
        location / {
            proxy_pass http://www.baidu.com
        }
        ...
    }
}
```

配置完后，重新加载`nginx -s reload`

当我访问该代理服务器ip，则会转到www.baidu.com

#### 6. 停止 nginx
若需要停止 nginx，则执行如下命令或ps & kill
```bash
killall nginx
```

#### 7. 实例讲解
最后讲一个实用例子，一台主机www.example.com有三个服务，分别对应三个端口(80, 81, 82)，我可以申请3个域名，分别对应这三个服务，配置如下：

test.example.com -> 代理服务器IP
test1.example.com -> 代理服务器IP
test2.example.com -> 代理服务器IP

```bash
    ...
    server {
        server_name test.example.com;
        ...
        location / {
            proxy_pass http://www.example.com:80;
        }
        ...
    }
    server {
        server_name test1.example.com;
        ...
        location / {
            proxy_pass http://www.example.com:81;
        }
        ...
    }
    server {
        server_name test2.example.com;
        ...
        location / {
            proxy_pass http://www.example.com:82;
        }
        ...
    }
```
这样我就可以不用为每个服务购买一台主机



