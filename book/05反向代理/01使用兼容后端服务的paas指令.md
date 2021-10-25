### 使用兼容后端服务的paas指令
[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-65)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 根据上游服务选取合适的`proxy_*`指令

- `http`: 使用`proxy_pass`
- `uWSGI`: 使用`uwsgi_pass`
- `FastCGI`: 使用`fastcgi_pass`

> 举例说明:

`uwsgi_pass`指令将使用`uwsgi`协议，`proxy_pass`使用普通的`HTTP`协议与`uWSGI`服务通信。
`uWSGI`文档称`uWSGI`协议更好，更快，可以受益于所有的`uWSGI`特性。

比如：你可以向`uWSGI`服务端发送信息，说明你发送数据的类型，以及应该调用什么`uWSGI`插件来生成响应。
而使用`proxy_pass`将不能使用该特性。

> 配置样例:

```nginx configuration
server {

  location /app/ {

    # backend layer: OpenResty as a front for app
    proxy_pass http://192.168.154.102:80;

  }

  location /app/v3 {

    # backend layer: uWSGI Python app
    uwsgi_pass 192.168.154.102:8080;

  }

  location /app/v4 {

    # backend layer: php-fpm app
    fastcgi_pass 192.168.154.102:8081;

  }
  ...

}
```




