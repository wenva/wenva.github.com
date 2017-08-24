---
layout: post
title: "linux下nginx反向代理配置"
date: 2018-08-24
comments: false
categories: linux
---

* 1. 安装 pcre
```bash
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.41.tar.gz
./configure
make
make install
```

* 2. 安装 nginx

```bash
wget http://nginx.org/download/nginx-1.13.4.tar.gz
tar xzvf nginx-1.13.4.tar.gz
cd nginx-1.13.4
./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module
make
make install
ln -s /usr/local/nginx/sbin/nginx /usr/local/bin
```

* 3. 运行nginx

```bash
nginx
```

若遇到找不到 pcre 动态库，则将/usr/local/lib加入系统动态库

```bash
echo '/usr/local/lib' >> /etc/ld.so.conf.d/local.conf
```

* 4. 添加用户组

```bash
groupadd nginx
useradd -g nginx nginx
```

* 5. 配置反向代理
vim /usr/local/nginx/conf/nginx.conf

```bash
user nginx nginx;
error_log  logs/error.log;
pid        logs/nginx.pid;
...
http {
    ...
    server {
        ...
        location / {
            proxy_pass http://www.baidu.com
            proxy_set_header Host www.baidu.com
        }
        ...
    }
}
```

配置完后，重新加载`nginx -s reload`

* 4. 停止 nginx
若需要停止 nginx，则执行如下命令或ps & kill
```bash
killall nginx
```





