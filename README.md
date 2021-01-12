- [安装部署](#%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2)
  - [编译安装](#%E7%BC%96%E8%AF%91%E5%AE%89%E8%A3%85)
  - [预编译安装](#%E9%A2%84%E7%BC%96%E8%AF%91%E5%AE%89%E8%A3%85)
- [集群方案](#%E9%9B%86%E7%BE%A4%E6%96%B9%E6%A1%88)
- [配置调优](#%E9%85%8D%E7%BD%AE%E8%B0%83%E4%BC%98)
- [配置样例](#%E9%85%8D%E7%BD%AE%E6%A0%B7%E4%BE%8B)
  - [https配置样例](#https%E9%85%8D%E7%BD%AE%E6%A0%B7%E4%BE%8B)
    - [自签](#%E8%87%AA%E7%AD%BE)
    - [开源](#%E5%BC%80%E6%BA%90)
- [安全加固](#%E5%AE%89%E5%85%A8%E5%8A%A0%E5%9B%BA)
  - [普通用户运行](#%E6%99%AE%E9%80%9A%E7%94%A8%E6%88%B7%E8%BF%90%E8%A1%8C)
  - [版本迭代更新](#%E7%89%88%E6%9C%AC%E8%BF%AD%E4%BB%A3%E6%9B%B4%E6%96%B0)
  - [隐藏版本信息](#%E9%9A%90%E8%97%8F%E7%89%88%E6%9C%AC%E4%BF%A1%E6%81%AF)
  - [隐藏目录禁止访问](#%E9%9A%90%E8%97%8F%E7%9B%AE%E5%BD%95%E7%A6%81%E6%AD%A2%E8%AE%BF%E9%97%AE)
  - [剔除无用模块](#%E5%89%94%E9%99%A4%E6%97%A0%E7%94%A8%E6%A8%A1%E5%9D%97)
  - [调整标识名称](#%E8%B0%83%E6%95%B4%E6%A0%87%E8%AF%86%E5%90%8D%E7%A7%B0)
  - [隐藏不安全头](#%E9%9A%90%E8%97%8F%E4%B8%8D%E5%AE%89%E5%85%A8%E5%A4%B4)
  - [配置ssl证书](#%E9%85%8D%E7%BD%AEssl%E8%AF%81%E4%B9%A6)
  - [引用最新依赖](#%E5%BC%95%E7%94%A8%E6%9C%80%E6%96%B0%E4%BE%9D%E8%B5%96)
  - [tls关闭gzip](#tls%E5%85%B3%E9%97%ADgzip)
  - [降低XSS劫持](#%E9%99%8D%E4%BD%8Exss%E5%8A%AB%E6%8C%81)
  - [配置Referrer-Policy](#%E9%85%8D%E7%BD%AEreferrer-policy)
  - [配置X-Frame-Option](#%E9%85%8D%E7%BD%AEx-frame-option)
  - [配置Feature-Policy](#%E9%85%8D%E7%BD%AEfeature-policy)
  - [禁用不安全HTTP方法](#%E7%A6%81%E7%94%A8%E4%B8%8D%E5%AE%89%E5%85%A8http%E6%96%B9%E6%B3%95)
  - [禁止缓存敏感数据](#%E7%A6%81%E6%AD%A2%E7%BC%93%E5%AD%98%E6%95%8F%E6%84%9F%E6%95%B0%E6%8D%AE)
  - [防止缓冲区溢出攻击](#%E9%98%B2%E6%AD%A2%E7%BC%93%E5%86%B2%E5%8C%BA%E6%BA%A2%E5%87%BA%E6%94%BB%E5%87%BB)
- [模块使用](#%E6%A8%A1%E5%9D%97%E4%BD%BF%E7%94%A8)
  - [健康检测模块](#%E5%81%A5%E5%BA%B7%E6%A3%80%E6%B5%8B%E6%A8%A1%E5%9D%97)
  - [waf功能使用](#waf%E5%8A%9F%E8%83%BD%E4%BD%BF%E7%94%A8)
- [nginx原理分析](#nginx%E5%8E%9F%E7%90%86%E5%88%86%E6%9E%90)
  - [location匹配顺序](#location%E5%8C%B9%E9%85%8D%E9%A1%BA%E5%BA%8F)
  - [http请求处理流程](#http%E8%AF%B7%E6%B1%82%E5%A4%84%E7%90%86%E6%B5%81%E7%A8%8B)
- [TODO](#todo)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 安装部署

**适用平台**

- CentOS

- RedHat

- 中标麒麟

## 编译安装

> 1、环境依赖

安装配置yum

> 2、内嵌模块说明

- ssl

- stream

- [ngx_cache_purge](https://github.com/FRiCKLE/ngx_cache_purge)

- [headers-more-nginx](https://github.com/openresty/headers-more-nginx-module)

- [naxsi](https://github.com/nbs-system/naxsi)

- nginx_upstream_check

- [LuaJIT](https://github.com/LuaJIT/LuaJIT)

> 3、检测yum可用性

尝试yum安装vim

	yum install -y vim
	echo $?

若返回值为0，证明安装完成，如非0说明yum有问题，[yum配置方式参考](https://github.com/weiliang-ms/wl-awesome/blob/master/linux/package/yum.md)

> 4、安装nginx

上传[安装包](https://github.com/wl-deploy/nginx/archive/latest.tar.gz)至目标服务器`/tmp`目录下，`root`执行：


	tar zxvf nginx-latest.tar.gz && cd nginx && sh install.sh && cd -


**编译过程大约耗时5~10分钟**

> 5、配置文件说明

- 主配置文件：`/opt/nginx/conf/nginx.conf`

- 自定义配置文件：`/opt/nginx/conf/conf.d/*.conf`

**即/opt/nginx/conf/conf.d/下创建以`.conf`结尾的文件，重载（reload）生效**

> 6、启停命令

启动

	/opt/nginx/sbin/nginx

关闭

	/opt/nginx/sbin/nginx -s stop

重载配置

	/opt/nginx/sbin/nginx -s reload


检测配置

	/opt/nginx/sbin/nginx -t
	
## 预编译安装

> 下载预编译包

根据操作系统选取对应版本

- [nginx-1.18.0-neu.el6.x86_64.rpm](https://github.com/wl-deploy/nginx/releases/download/latest/nginx-1.18.0-neu.el6.x86_64.rpm)
- [nginx-1.18.0-neu.el7.x86_64.rpm](https://github.com/wl-deploy/nginx/releases/download/latest/nginx-1.18.0-neu.el7.x86_64.rpm)

> 上传安装

    rpm -vih nginx-*-neu.el?.x86_64.rpm
    
> 启动

    /opt/nginx/sbin/nginx

# 集群方案

- keepalive软件 + 虚拟IP

- 负载均衡设备

**推荐硬件负载均衡设备（如F5|A10|深信服等）**

> 1、申请虚拟IP

该IP为浮动IP，与`nginx`节点IP `vlan id`需一致,并需要备案以免IP冲突

> 2、安装keepalived

所有`nginx`节点(至少两个节点)安装keepalived

	yum install -y keepalived

> 3、配置keepalived

**主节点配置**

	cat > /etc/keepalived/keepalived.conf <<-'EOF'
	! Configuration File for keepalived
	
	global_defs {
	   router_id master
	}
	
	vrrp_instance VI_1 {
	    state MASTER
	    interface ens33
	    virtual_router_id 51
	    priority 150
	    advert_int 1
	    authentication {
	        auth_type PASS
	        auth_pass weiliang
	    }
	    virtual_ipaddress {
	        172.16.145.200/24
	    }
	}
	EOF

**从节点配置**

	cat > /etc/keepalived/keepalived.conf <<-'EOF'
	! Configuration File for keepalived
	
	global_defs {
	   router_id bakup
	}
	
	vrrp_instance VI_1 {
	    state BAKUP
	    interface ens33
	    virtual_router_id 51
	    priority 150
	    advert_int 1
	    authentication {
	        auth_type PASS
	        auth_pass weiliang
	    }
	    virtual_ipaddress {
	        172.16.145.200/24
	    }
	}
	EOF

**需要调整内容：**

- 网卡接口名称:
`interface ens33` 改为实际接口名称(`ip a`获取)

- 虚拟IP地址:
`172.16.145.200` 改为实际虚拟IP地址

> 4、启动keepalived

**CentOS7|Red Hat 7**

	systemctl enable keepalived --now

**CentOS6|Red Hat 6**

	service keepalived start
	chkconfig keepalived on

# 配置调优

> upstream 配置 keepalive

	upstream backend-server {
	server 192.168.1.2:8080;
	keepalive 16;
	}

	server {
		listen 8080;
		location / {
			# Default is HTTP/1, keepalive is only enabled in HTTP/1.1:
		    proxy_http_version  1.1;
		    # Remove the Connection header if the client sends it,
		    # it could be "close" to close a keepalive connection:
		    proxy_set_header    Connection "";
			proxy_pass http://backend-server;
		}
	}

	#nginx upstream{}默认与上游服务以HTTP1.0进行通信，不具备keepalive能力

# 配置样例
	
## https配置样例

获取ssl证书

- 购买

- 自签

- [第三方免费](https://letsencrypt.org/)

### 自签

> 1、自签证书

自签脚本`ssl.sh`内容

	export domain=www.example.com # 域名
	
	export address=192.168.1.11 # IP地址（可选）
	
	export contryName=CN # 国家
	
	export stateName=Liaoning # 省/州/邦
	
	export locationName=Shenyang # 地方/城市名
	
	export organizationName=example # 组织/公司名称
	
	export sectionName=develop # 组织/公司部门名称
	
	echo "Getting Certificate Authority..."
	openssl genrsa -out ca.key 4096
	openssl req -x509 -new -nodes -sha512 -days 3650 \
	  -subj "/C=$contryName/ST=$stateName/L=$locationName/O=$organizationNaem/OU=$sectionName/CN=$domain" \
	  -key ca.key \
	  -out ca.crt
	
	echo "Create your own Private Key..."
	openssl genrsa -out nginx.key 4096
	
	echo "Generate a Certificate Signing Request..."
	openssl req -sha512 -new \
	  -subj "/C=$contryName/ST=$stateName/L=$locationName/O=$organizationNaem/OU=$sectionName/CN=$domain" \
	  -key nginx.key \
	  -out $domain.csr
	
	echo "Generate the certificate of your registry host..."
	cat > v3.ext <<-EOF
	authorityKeyIdentifier=keyid,issuer
	basicConstraints=CA:FALSE
	keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
	extendedKeyUsage = serverAuth
	subjectAltName = @alt_names
	[alt_names]
	DNS.1=$domain
	DNS.2=hostname
	IP.1=$address
	EOF
	openssl x509 -req -sha512 -days 3650 \
	  -extfile v3.ext \
	  -CA ca.crt -CAkey ca.key -CAcreateserial \
	  -in $domain.csr \
	  -out nginx.crt
	
	echo "Convert server nginx.crt to $domain.cert..."
	openssl x509 -inform PEM -in nginx.crt -out $domain.cert
	
	echo "merge the intermediate certificate with your own certificate to create a certificate bundle..."
	cp nginx.crt /etc/pki/ca-trust/source/anchors/nginx.crt
	update-ca-trust
	
	echo "successful..."


**需要调整内容：**

	export domain=www.example.com # 域名
	
	export address=192.168.1.11 # IP地址（可选）
	
	export contryName=CN # 国家
	
	export stateName=Liaoning # 省/州/邦
	
	export locationName=Shenyang # 地方/城市名
	
	export organizationName=example # 组织/公司名称
	
	export sectionName=develop # 组织/公司部门名称

**nginx所在服务器执行:**

	mkdir -p /opt/ssl && cd /opt/ssl && sh ssl.sh

**配置样例:**

	server {
	    listen 5443 ssl;
	    ssl_protocols TLSv1.2;
	    ssl_prefer_server_ciphers on;
	    ssl_session_cache shared:SSL:10m;
	    ssl_certificate /opt/ssl/nginx.crt;
	    ssl_certificate_key /opt/ssl/nginx.key;
	...其他Location配置...
	}


### 开源

> 免费ssl社区证书

[Let's encrypt](https://www.jianshu.com/p/0d455c7a9326)

**环境依赖:**

- 域名备案

- 边界服务器（域名绑定的主机）可访问互联网

> 基于IP签发ssl证书

[DVSSL](https://www.sslzhengshu.com/validation/ip-ssl.html)

# 安全加固

[参考开源项目](https://github.com/trimstray/nginx-admins-handbook#hardening)

## 普通用户运行

> 非root用户运行

	nginx.conf -> user xxx;

## 版本迭代更新

> 不间断的更新版本

由于新版本会解决旧版本Bug等，建议每次官方稳定版出来一周后进行nginx升级。

## 隐藏版本信息

> 隐藏版本信息

`nginx.conf`中

	http {
		...
		server_tokens off;	
		...
	}

## 隐藏目录禁止访问

> 敏感文件禁止访问

**如.git .svn等**

	server {
		...
		location ~* ^.*(\.(?:git|svn|htaccess))$ {
	  		return 403;
		}
		...
	}

## 剔除无用模块

> 剔除无用模块

**源码编译时剔除未使用的模块**

	./configure --without-http_autoindex_module
	
## 调整标识名称

> 修改nginx server标识

[原因说明](https://www.troyhunt.com/shhh-dont-let-your-response-headers/)

**nginx.conf中添加（需要编译时引入ngx_headers_more模块）**

	http {
		...
		more_set_headers "Server: Unknown";
		...
	}

## 隐藏不安全头

> 剔除不安全HEADER

[参考地址](https://veggiespam.com/headers/)

	location / {
		proxy_hide_header X-Powered-By;
		proxy_hide_header X-AspNetMvc-Version;
		proxy_hide_header X-AspNet-Version;
		proxy_hide_header X-Drupal-Cache;
		proxy_pass http://backend-server;
	}

## 配置ssl证书

一般配置tls证书时需要用到以下配置

	ssl_protocols TLSv1.2;
	ssl_prefer_server_ciphers on;

## 引用最新依赖

> 使用最新版openssl

[openssl项目地址](https://www.openssl.org/policies/releasestrat.html)

**系统自带的一般版本不是最新的，建议自己编译安装**

**关于openssl版本维护信息**

- the next version of OpenSSL will be 3.0.0

- version 1.1.1 will be supported until 2023-09-11 (LTS)

- last minor version: 1.1.1c (May 23, 2019)

- version 1.1.0 will be supported until 2019-09-11

- last minor version: 1.1.0k (May 28, 2018)

- version 1.0.2 will be supported until 2019-12-31 (LTS)

- last minor version: 1.0.2s (May 28, 2018)

## tls关闭gzip

Some attacks are possible (e.g. the real BREACH attack is a complicated) because of gzip (HTTP compression not TLS compression) being enabled on SSL requests. 

In most cases, the best action is to simply disable gzip for SSL.

	gzip off;

## 降低XSS劫持

	add_header Content-Security-Policy "default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src 'self';" always;
	add_header X-XSS-Protection "1; mode=block" always;

## 配置Referrer-Policy

[refer介绍](https://scotthelme.co.uk/a-new-security-header-referrer-policy/)
	
http请求分为请求行，请求头以及请求体，而请求头又分为general，request headers，此字段设置与general中，用来约定request headers中的referer

任何情况下都不发送referer

	add_header Referrer-Policy "origin";

**可选值**

	"no-referrer",                     #任何情况下都不发送referer
	"no-referrer-when-downgrade",      #在同等安全等级下（例如https页面请求https地址），发送referer，但当请求方低于发送方（例如https页面请求http地址），不发送referer
	"same-origin",                     #当双方origin相同时发送
	"origin",                          #仅仅发送origin，即protocal+host
	"strict-origin",                   #当双方origin相同且安全等级相同时发送
	"origin-when-cross-origin",        #跨域时发送origin
	"strict-origin-when-cross-origin",
	"unsafe-url"                       #任何情况下都显示完整的referer

## 配置X-Frame-Option

	add_header X-Frame-Options "SAMEORIGIN" always;

## 配置Feature-Policy

Feature Policy是一个新的http响应头属性，允许一个站点开启或者禁止一些浏览器属性和API，来更好的确保站点的安全性和隐私性。 可以严格的限制站点允许使用的属性是很愉快的，而可以对内嵌在站点中的iframe进行限制则更加增加了站点的安全性。

**W3C标准**

[https://w3c.github.io/webappsec-feature-policy/](https://w3c.github.io/webappsec-feature-policy/)

	add_header Feature-Policy "geolocation 'none'; midi 'none'; notifications 'none'; push 'none'; sync-xhr 'none'; microphone 'none'; camera 'none'; magnetometer 'none'; gyroscope 'none'; speaker 'none'; vibrate 'none'; fullscreen 'none'; payment 'none'; usb 'none';";

## 禁用不安全HTTP方法

	if ($request_method !~ ^(GET|POST|HEAD)$) {
  		return 405;
	}

## 禁止缓存敏感数据

	expires 0;
    add_header Cache-Control "no-cache, no-store";

## 防止缓冲区溢出攻击

	client_max_body_size    100m;

	client_body_buffer_size 128k;

	client_header_buffer_size 512k;

	large_client_header_buffers 4 512k

# 模块使用
## 健康检测模块

**目的：保证负载高可用**

配置样例：

`/opt/nginx/conf/conf.d/test.conf`

	upstream backend-server {
	server 127.0.0.1:8080;
	# health check
	check interval=5000 rise=2 fall=3 timeout=1000 type=http;
	check_http_send "GET /api/actuator/health HTTP/1.0\r\n\r\n";
	check_http_expect_alive http_2xx http_3xx;
	keepalive 16;
	}
	
	server {
	  listen 8081;
	  location /api {
	    proxy_pass http://backend-server;
	    include conf.d/http.proxy;
	  }
	  location / {
	    alias /opt/nginx/static/frontend/;
	  }
	}

[项目官方地址](https://github.com/yaoweibin/nginx_upstream_check_module)
	
## waf功能使用

基于[ngx_lua_waf](https://github.com/loveshell/ngx_lua_waf)项目更改部分内容

**该模块可导致nginx主动断开client连接或nginx 402状态码返回，可查看/opt/nginx/logs/waf.log定位拦截规则**

核心功能说明：

- host白名单

- referer白名单

- http方法白名单

- agent黑白名单

-  url黑名单


`/opt/nginx/conf/nginx.conf`引用配置


	http {
		...
		lua_package_path "/opt/nginx/conf/waf/?.lua";
		lua_shared_dict limit 10m;
		init_by_lua_file  conf/waf/init.lua;
		access_by_lua_file conf/waf/access.lua;
		...
	}

**waf开关**

`/opt/nginx/conf/waf/config.lua`内容介绍

	# 是否开启waf，默认true，可选（true|false），总开关，若置为false以下配置不生效
	open_waf=true
	# 检测url规则黑名单文件为 /opt/nginx/conf/waf/black/url(主要拦截请求隐藏文件及活体检测端点等)
	open_check_url=false
	# 检测args规则黑名单文件为 /opt/nginx/conf/waf/black/args(主要拦截非法注入等)
	open_check_agrs=false
	# 检测host合法性，文件为 /opt/nginx/conf/waf/white/host，除配置文件内以外的host全视为非法Host
	open_check_host=false
	# referer白名单，文件为 /opt/nginx/conf/waf/white/referer
	open_check_referer=false
	open_check_agent=false
	# http方法，白名单/opt/nginx/conf/waf/white/method
	open_check_method=false
	# 检测body（空body，非法内容等）
	open_check_body=false
	white_rule_path="/opt/nginx/conf/waf/white/"
	black_rule_path="/opt/nginx/conf/waf/black/"
	log_path="/opt/nginx/logs/"
	open_logging=true

# nginx原理分析
## location匹配顺序

**例子来源以下地址**

[nginx-admins-handbook](https://github.com/trimstray/nginx-admins-handbook#introduction)

> 假设配置如下

	server {

	 listen           80;
	 server_name      xyz.com www.xyz.com;
	
	 location ~ ^/(media|static)/ {
	  root            /var/www/xyz.com/static;
	  expires         10d;
	 }
	
	 location ~* ^/(media2|static2) {
	  root            /var/www/xyz.com/static2;
	  expires         20d;
	 }
	
	 location /static3 {
	  root            /var/www/xyz.com/static3;
	 }
	
	 location ^~ /static4 {
	  root            /var/www/xyz.com/static4;
	 }
	
	 location = /api {
	  proxy_pass      http://127.0.0.1:8080;
	 }
	
	 location / {
	  proxy_pass      http://127.0.0.1:8080;
	 }
	
	 location /backend {
	  proxy_pass      http://127.0.0.1:8080;
	 }
	
	 location ~ logo.xcf$ {
	  root            /var/www/logo;
	  expires         48h;
	 }
	
	 location ~* .(png|ico|gif|xcf)$ {
	  root            /var/www/img;
	  expires         24h;
	 }
	
	 location ~ logo.ico$ {
	  root            /var/www/logo;
	  expires         96h;
	 }
	
	 location ~ logo.jpg$ {
	  root            /var/www/logo;
	  expires         48h;
	 }
	
	}

> 匹配规则如下

<table>
<thead>
<tr>
<th align="center"><b>请求URL</b></th>
<th align="center"><b>相匹配的location</b></th>
<th align="center"><b>最终匹配</b></th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>/</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code></td>
<td align="left"><code>/</code></td>
</tr>
<tr>
<td align="left"><code>/css</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code></td>
<td align="left"><code>/</code></td>
</tr>
<tr>
<td align="left"><code>/api</code></td>
<td align="left"><sup>1)</sup> exact match for <code>/api</code></td>
<td align="left"><code>/api</code></td>
</tr>
<tr>
<td align="left"><code>/api/</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code></td>
<td align="left"><code>/</code></td>
</tr>
<tr>
<td align="left"><code>/backend</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> prefix match for <code>/backend</code></td>
<td align="left"><code>/backend</code></td>
</tr>
<tr>
<td align="left"><code>/static</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code></td>
<td align="left"><code>/</code></td>
</tr>
<tr>
<td align="left"><code>/static/header.png</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case sensitive regex match for <code>^/(media|static)/</code></td>
<td align="left"><code>^/(media|static)/</code></td>
</tr>
<tr>
<td align="left"><code>/static/logo.jpg</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case sensitive regex match for <code>^/(media|static)/</code></td>
<td align="left"><code>^/(media|static)/</code></td>
</tr>
<tr>
<td align="left"><code>/media2</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case insensitive regex match for <code>^/(media2|static2)</code></td>
<td align="left"><code>^/(media2|static2)</code></td>
</tr>
<tr>
<td align="left"><code>/media2/</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case insensitive regex match for <code>^/(media2|static2)</code></td>
<td align="left"><code>^/(media2|static2)</code></td>
</tr>
<tr>
<td align="left"><code>/static2/logo.jpg</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case insensitive regex match for <code>^/(media2|static2)</code></td>
<td align="left"><code>^/(media2|static2)</code></td>
</tr>
<tr>
<td align="left"><code>/static2/logo.png</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case insensitive regex match for <code>^/(media2|static2)</code></td>
<td align="left"><code>^/(media2|static2)</code></td>
</tr>
<tr>
<td align="left"><code>/static3/logo.jpg</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/static3</code><br><sup>2)</sup> prefix match for <code>/</code><br><sup>3)</sup> case sensitive regex match for <code>logo.jpg$</code></td>
<td align="left"><code>logo.jpg$</code></td>
</tr>
<tr>
<td align="left"><code>/static3/logo.png</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/static3</code><br><sup>2)</sup> prefix match for <code>/</code><br><sup>3)</sup> case insensitive regex match for <code>.(png|ico|gif|xcf)$</code></td>
<td align="left"><code>.(png|ico|gif|xcf)$</code></td>
</tr>
<tr>
<td align="left"><code>/static4/logo.jpg</code></td>
<td align="left"><sup>1)</sup> priority prefix match for <code>/static4</code><br><sup>2)</sup> prefix match for <code>/</code></td>
<td align="left"><code>/static4</code></td>
</tr>
<tr>
<td align="left"><code>/static4/logo.png</code></td>
<td align="left"><sup>1)</sup> priority prefix match for <code>/static4</code><br><sup>2)</sup> prefix match for <code>/</code></td>
<td align="left"><code>/static4</code></td>
</tr>
<tr>
<td align="left"><code>/static5/logo.jpg</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case sensitive regex match for <code>logo.jpg$</code></td>
<td align="left"><code>logo.jpg$</code></td>
</tr>
<tr>
<td align="left"><code>/static5/logo.png</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case insensitive regex match for <code>.(png|ico|gif|xcf)$</code></td>
<td align="left"><code>.(png|ico|gif|xcf)$</code></td>
</tr>
<tr>
<td align="left"><code>/static5/logo.xcf</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case sensitive regex match for <code>logo.xcf$</code></td>
<td align="left"><code>logo.xcf$</code></td>
</tr>
<tr>
<td align="left"><code>/static5/logo.ico</code></td>
<td align="left"><sup>1)</sup> prefix match for <code>/</code><br><sup>2)</sup> case insensitive regex match for <code>.(png|ico|gif|xcf)$</code></td>
<td align="left"><code>.(png|ico|gif|xcf)$</code></td>
</tr>
</tbody>
</table>

> 匹配顺序说明

`nginx根据uri进行最优匹配`

<ol>
<li>
<p>基于前缀的NGINX位置匹配(没有正则表达式)。每个位置都将根据请求URI进行检查</p>
</li>
<li>
<p>NGINX搜索精确的匹配。如果=修饰符与请求URI完全匹配，则立即选择此特定位置块</p>
</li>
<li>
<p>如果没有找到精确的位置块(即没有相应的=修饰符)，NGINX将继续使用非精确的前缀。它从这个URI的最长匹配前缀位置开始，方法如下:</p>
<ul>
<li>
<p>如果最长匹配前缀位置有^~修饰符，NGINX将立即停止搜索并选择该位置。</p>
</li>
<li>
<p>假设最长匹配前缀位置不使用^~修饰符，匹配将被临时存储，并继续执行。</p>
</li>
</ul>
</li>
<li>
<p>一旦选择并存储了最长匹配前缀位置，NGINX就会继续计算区分大小写和不敏感的正则表达式位置。第一个适合URI的正则表达式位置将立即被选中来处理请求</p>
</li>
<li>
<p>如果没有找到匹配请求URI的正则表达式位置，则选择先前存储的前缀位置来服务请求</p>
</li>
</ol>

## http请求处理流程

**参考文章**

[nginx-admins-handbook](https://github.com/trimstray/nginx-admins-handbook#introduction "参考文章")

[博客](https://blog.51cto.com/wenxi123/2296295?source=dra)

**nginx处理一个请求共分为11个阶段**

> 阶段一，NGX_HTTP_POST_READ_PHASE

	获取请求头信息
	#相关模块: ngx_http_realip_module

> 阶段二，NGX_HTTP_SERVER_REWRITE_PHASE

	实现在server{}块中定义的重写指令:
	使用PCRE正则表达式更改请求uri，返回重定向uri；
	#相关模块: ngx_http_rewrite_module

> 阶段三，NGX_HTTP_FIND_CONFIG_PHASE

	**仅nginx核心模块可以参与**
	根据阶段二的uri匹配location

> 阶段四，NGX_HTTP_REWRITE_PHASE

	由阶段三匹配到location，并在location{}块中再次进行uri转换
	#相关模块: ngx_http_rewrite_module

> 阶段五，NGX_HTTP_POST_REWRITE_PHASE

	**仅nginx核心模块可以参与**
	请求地址重写提交阶段，防止递归修改uri造成死循环，（一个请求执行10次就会被nginx认定为死循环）
	#相关模块: ngx_http_rewrite_module

> 阶段六，NGX_HTTP_PREACCESS_PHASE

	访问控制阶段一：
	验证预处理请求限制，访问频率、连接数限制（访问限制）
	#相关模块：ngx_http_limit_req_module, ngx_http_limit_conn_module, ngx_http_realip_module

> 阶段七，NGX_HTTP_ACCESS_PHASE

	访问控制阶段二：
	客户端验证(源IP是否合法，是否通过HTTP认证)
	#相关模块：ngx_http_access_module, ngx_http_auth_basic_module

> 阶段八，NGX_HTTP_POST_ACCESS_PHASE

	**仅nginx核心模块可以参与**
	访问控制阶段三：
	访问权限检查提交阶段；如果请求不被允许访问nginx服务器，该阶段负责向用户返回错误响应；
	#相关模块：ngx_http_access_module, ngx_http_auth_basic_module

> 阶段九，NGX_HTTP_PRECONTENT_PHASE

	**仅nginx核心模块可以参与**
	如果http请求访问静态文件资源，try_files配置项可以使这个请求顺序地访问多个静态文件资源，直到某个静态文件资源符合选取条件
	#相关模块：ngx_http_try_files_module

> 阶段十，NGX_HTTP_CONTENT_PHASE

	内容产生阶段，大部分HTTP模块会介入该阶段，是所有请求处理阶段中最重要的阶段，因为这个阶段的指令通常是用来生成HTTP响应内容的；

	#相关模块：ngx_http_index_module, ngx_http_autoindex_module, ngx_http_gzip_module

> 阶段十一，NGX_HTTP_LOG_PHASE

	记录日志阶段
	#相关模块：ngx_http_log_module

> 示例图

![request-flow.png](https://upload-images.jianshu.io/upload_images/1967881-0f25f669eea357c2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# TODO

> 调整nginx目录

> rpm支持普通用户

> 更新依赖版本