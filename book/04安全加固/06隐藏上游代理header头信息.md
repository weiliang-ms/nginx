### 隐藏上游代理报头

[Hide upstream proxy headers](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-41)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

当`nginx`被用来反向代理上游服务器(比如一个`PHP-fpm`实例)时，
隐藏在上游响应中发送的某些报头(比如PHP运行的版本)是有益的。

可以使用`proxy_hide_header`(或Lua模块)来隐藏/删除上游服务器返回到你的`nginx`反向代理(并最终返回到客户端)的头文件。

> 使用方式

代理`http`服务的`location`块添加`include /etc/nginx/conf/conf.d/hide-headers.rule;`配置

```nginx configuration
upstream ddd-server {
server 11.11.11.11:80;
server 11.11.11.12:80; 
}
server {
    listen 8081;
    location /ddd {
        include /etc/nginx/conf/conf.d/hide-headers.rule;
        proxy_pass http://ddd-server;
    }
}
```

`/etc/nginx/conf/conf.d/hide-headers.rule`: 

```nginx configuration
proxy_hide_header X-Application-Context;
proxy_hide_header Access-Control-Allow-Origin;
proxy_hide_header X-Powered-By;
proxy_hide_header X-AspNetMvc-Version;
proxy_hide_header X-Drupal-Cache;
proxy_hide_header X-Powered-By;
proxy_hide_header Server;
proxy_hide_header X-AspNet-Version;
proxy_hide_header X-Drupal-Dynamic-Cache;
proxy_hide_header X-Generator;
proxy_hide_header X-Runtime;
proxy_hide_header X-Rack-Cache;
```