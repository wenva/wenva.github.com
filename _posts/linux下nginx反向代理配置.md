# linux下nginx反向代理配置

* 安装 pcre
```bash
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.41.tar.gz
./configure
make
make install
```

* 安装 nginx

```bash
wget http://nginx.org/download/nginx-1.13.4.tar.gz
tar xzvf nginx-1.13.4.tar.gz
cd nginx-1.13.4
./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module
make
make install
ln -s /usr/local/nginx/sbin/nginx /usr/local/bin
```

* 运行 nginx


* 停止 nginx

```bash
killall nginx
```



* 配置




