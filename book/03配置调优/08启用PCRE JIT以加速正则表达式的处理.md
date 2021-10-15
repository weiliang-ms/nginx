### 使用return代替rewrite做重定向

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#beginner-enable-pcre-jit-to-speed-up-processing-of-regular-expressions)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 解释说明

1. 正则检查规则可能非常耗时，尤其是复杂的正则表达式(regex)条件，允许对正则表达式使用`JIT`可以加快处理速度。
2. 通过使用`PCRE`库编译`NGINX`，可以用`location`块执行复杂的操作，并使用强大的`rewrite`指令
3. 

> 使用样例

- 不建议实现方式

```nginx configuration
```

- 建议实现方式

```nginx configuration

```
