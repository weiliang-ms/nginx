### 隐藏版本信息
[Hide Nginx version number](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-39)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 隐藏版本信息(已内置)

```nginx configuration
server_tokens off;
```

> 修改`server`信息(已内置)

```nginx configuration
more_set_headers "Server: Unknown";
```

> 错误页

TODO


