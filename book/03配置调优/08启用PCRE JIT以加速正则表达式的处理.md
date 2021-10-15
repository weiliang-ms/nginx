### 使用return代替rewrite做重定向

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#beginner-enable-pcre-jit-to-speed-up-processing-of-regular-expressions)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 使用`pcre_jit`的优势

正则检查规则可能非常耗时，尤其是复杂的正则表达式(regex)条件，允许对正则表达式使用`JIT`可以加快处理速度。 

通过使用`PCRE`库编译`NGINX`，可以用`location`块执行复杂的操作，并使用强大的`rewrite`指令

`PCRE JIT`规则匹配引擎可以显著提高正则表达式的处理速度，带有`pcre_jit`的`NGINX`比没有它的`NGINX`快很多（处理正则表达式）。
这个选项可以提高性能。

> 使用`pcre_jit`的劣势

在某些情况下，`pcre_jit`可能有负面影响，具体参考[PCRE性能优化](../优秀文档/PCRE性能优化.md)

> 启用方式

- `pcre8.20+`
- `nginx`编译时添加参数: `--with-pcre=path_to_pcre8.20+ --with-pcre-jit`

> 使用方式

```nginx configuration
http {
    ...
    pcre_jit on;
    ...
}
```