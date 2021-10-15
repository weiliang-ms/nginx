### 使用return代替rewrite做重定向

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#beginner-use-return-directive-instead-of-rewrite-for-redirects)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 解释说明

1. `NGINX`中重写`url`的能力是一个非常强大和重要的特性，从技术角度讲`return`与`rewrite`均能实现。
但使用`return`相对`rewrite`更简单和更快，因为计算`RegEx`会产生额外的系统开销。
2. `Return`指令可以立即停止处理请求(它直接停止执行)并将指定的代码返回给客户端，省略了正则计算的流程。
3. 如果你需要用`regex`验证`URL`或者需要获取原始`URL`中的元素(显然不在相应的`NGINX`变量中)，那么你应该使用`rewrite`

> 使用样例

- 不建议实现方式

```nginx configuration
server {

...

location / {

    try_files $uri $uri/ =404;

    rewrite ^/(.*)$ https://example.com/$1 permanent;

}

...

}
```

- 建议实现方式

```nginx configuration
server {

  ...

  location / {

    try_files $uri $uri/ =404;

    return 301 https://example.com$request_uri;

  }

  ...

}
```
