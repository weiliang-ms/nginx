![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/weiliang-ms/nginx-rpm/build-el7?style=flat-square)
![GitHub all releases](https://img.shields.io/github/downloads/weiliang-ms/nginx-rpm/total?style=flat-square)
![GitHub](https://img.shields.io/github/license/weiliang-ms/easyctl?style=flat-square)

## 适用场景

- 一键式安装`nginx`，无需安装其依赖（如zlib-devel|pcre-devel|openssl-devel）
- 安全可控：可随时更新依赖包版本、模块包版本、`nginx`版本，降低软件漏洞所带来的风险

## 优势

内置如下模块/特性:

- 内嵌模块
  - [修改http头模块](https://github.com/openresty/headers-more-nginx-module)
  - [waf模块](https://github.com/loveshell/ngx_lua_waf)
- 特性列表
  - [日志文件轮转](https://linux.cn/article-4126-1.html)
  - [配置文件语法高亮](https://www.cnblogs.com/manastudent/p/12936546.html)
  - [ip_hash支持基于主机号hash](https://blog.csdn.net/yswKnight/article/details/107180893)
  - 内置ssl生成工具

## 特性样例

### 配置ssl

**适用于测试环境（自签证书）**

1. 生成证书

```shell
cd /etc/nginx/ssl
/usr/sbin/generate-ssl.sh
```

2. 配置`ssl`代理

生成配置文件，对配置文件内容变更,`ssl`部分不变。
```shell
cd /etc/nginx/conf/conf.d
cp example/ssl.conf.example ssl.conf
```

调整后样例如下:

```shell
server {
    listen 5443 ssl;
    ssl_protocols TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_certificate /etc/ssl/nginx.crt;
    ssl_certificate_key /etc/ssl/nginx.key;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8080
    }
}
```

3. 查看监听是否生效

```shell
[root@localhost conf.d]# ss -aln|grep 5443
tcp    LISTEN     0      128       *:5443                  *:*
```

4. 重载

```shell
systemctl reload nginx
```

5. 启动`8080`监听

```shell
python -m SimpleHTTPServer 8080
```

6. 防火墙开放`5443`端口

- `CentOS6`

```shell
iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 5443 -j ACCEPT
/etc/rc.d/init.d/iptables save
service iptables restart
```

- `CentOS7`

```shell
firewall-cmd --zone=public --add-port=5443/tcp --permanent
firewall-cmd --reload
```

8. 浏览器访问`nginx`宿主机的`5443`端口验证`ssl`

### 构建介质

- [pcre](https://sourceforge.net/projects/pcre/files/pcre/8.45/pcre-8.45.tar.gz/download)