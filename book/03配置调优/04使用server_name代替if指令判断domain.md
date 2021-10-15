### 不要使用if指令判断domain

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#beginner-use-exact-names-in-a-server_name-directive-if-possible)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 原理分析

当`NGINX`接收到一个请求时，如果你配置了`if`指令用于检查每个请求的`Host`头，
不管请求的子域是什么，无论是`www.example.com`，还是`example.com`，都将执行该`if`指令进行判断。

相反，使用两个`server`指令，如下面的例子所示。这种方法降低了`NGINX`处理需求。

> 样例

- 错误的实现方式:

```nginx configuration
server {

  server_name example.com www.example.com;

  if ($host = www.example.com) {

    return 301 https://example.com$request_uri;
  }
  server_name example.com;
  ...

}
```

- 正确的实现方式:

```nginx configuration
server {

    listen 192.168.252.10:80;

    server_name www.example.com;

    return 301 $scheme://example.com$request_uri;

    # If you force your web traffic to use HTTPS:
    # return 301 https://example.com$request_uri;

    ...

}

server {

    listen 192.168.252.10:80;

    server_name example.com;

    ...

}
```

> 其他场景

不光`$server_name`指令，当判断`$scheme`值时，也应该用多个`server`代替`if`判断如。
在某些情况下(但并非总是如此)，添加一个额外的块指令比使用`if`更好。

> 官方建议：

在`location`上下文中使用`if`会存在一些问题，尽量避免。