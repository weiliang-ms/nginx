### 开启limit_conn限制下载速度

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-32)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

`nginx`提供了两个指令限制下载速度：
- `limit_rate_after`: 设置`limit_rate`指令生效前(未限速前)可传输的数据量
- `limit_rate`: 允许您限制单个客户端连接的传输速率(超过`limit_rate_after`)

以上两个指令限制了`nginx`每次连接的下载速度，所以，如果一个用户打开`x`个视频文件，它将能够下载`x *`他连接到视频文件的个数。

> 使用样例

```nginx configuration
# Create limit connection zone:
limit_conn_zone $binary_remote_addr zone=conn_for_remote_addr:1m;

# Add rules to limiting the download speed:
limit_rate_after 1m;  # run at maximum speed for the first 1 megabyte
limit_rate 250k;      # and set rate limit after 1 megabyte

# Enable queue:
location /videos {

  # Max amount of data by one client: 10 megabytes (limit_rate_after * 10)
  limit_conn conn_for_remote_addr 10;
  ...
}
```

