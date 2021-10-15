### 使用$request_uri代替正则

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#beginner-use-request_uri-to-avoid-using-regular-expressions)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 原理分析

1. 使用内置的`$request_uri`，我们可以有效地避免任何捕获或匹配操作(cpu计算)，通常正则批量会增加`CPU`开销，从而降低系统整体性能
2. 当规则为变换`Host`时（URI不变），直接使用`$request_uri`拼接新`host`更加高效。
3. `$request_uri`的值总是从客户端接收到的原始`URI`(带参数的完整原始请求`URI`)，与`$URI`指令相比不受任何规范化的约束
4. 如果你需要匹配`URI`和它的查询字符串，可以在`map`指令中使用`$request_uri`
5. 如果不加考虑地使用`$request_uri`会导致许多奇怪的行为。例如，在错误的地方使用`$request_uri`可能会导致`URL`编码字符变成双编码。
所以大多数时候你应使用`$uri`，因为它是标准化的。

> 样例

- 不建议实现方式

```nginx configuration
# 1)
rewrite ^/(.*)$ https://example.com/$1 permanent;

# 2)
rewrite ^ https://example.com$request_uri permanent;
```

- 建议实现方式

```nginx configuration
return 301 https://example.com$request_uri;
```



