## proxy_pass中使用$request_uri代替$uri

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-72)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 传递原生请求信息:

我认为将未更改的`URI`传递到上游服务的最佳规则是使用`proxy_pass http://<backend>`，不带任何参数（`uri`等部分）。


> 如果你需要对`proxy_pass`的上游服务`uri`做处理，请使用`$request_uri`参数而代替`$uri`参数

例如，在`proxy_pass`指令中不小心使用`$uri`会导致`http`头注入漏洞，
因为`URL`编码字符会被解码(这有时很重要，并不等同于`$request_uri`)。

更重要的是，`$uri`的值可能会在请求处理过程中改变，例如在进行内部重定向时，或者在使用索引文件时。


- 不建议的配置方式:

```nginx configuration
location /foo {

  proxy_pass http://django_app_server$uri;

}
```

- 建议的配置方式:

```nginx configuration
location /foo {

  proxy_pass http://django_app_server$request_uri;

}
```

- 最佳配置（不做任何处理）:

```nginx configuration
location /foo {

  proxy_pass http://django_app_server;

}
```