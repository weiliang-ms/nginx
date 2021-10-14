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