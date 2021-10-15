### 使用try_files指令来确保文件存在

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#beginner-use-try_files-directive-to-ensure-a-file-exists)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 解释说明

`try_files`绝对是一个非常有用的指令：你可以使用`try_files`指令来检查文件是否按照指定的顺序存在。

1. 应该使用`try_files`代替`if`指令，因为`if`指令的效率非常低，因为它对每个请求都进行判断
2. 使用`try_files`的优点是：只需一个命令就可以立即切换行为，代码也更易读。
3. `try_files`指令允许你：
- 检查文件是否存在于预定义列表中
- 检查指定目录中是否存在该文件
- 如果没有找到任何文件，则使用内部重定向

> 使用样例

- 不建议实现方式
```nginx configuration
server {

  ...

  root /var/www/example.com;

  location /images {

    if (-f $request_filename) {

      expires 30d;
      break;

    }

  ...

}

```
- 建议实现方式
```nginx configuration
server {

  ...

  root /var/www/example.com;

  location /images {

    try_files $uri =404;

  ...

}
```


