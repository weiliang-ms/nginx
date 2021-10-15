### upstream开启keepalive

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-31)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

> 解释说明

配置`keepalive`的主要意图：解决在高延迟网络上建立`TCP`连接的延迟问题。
当`nginx`与上游服务器之间需要持续保持一定数量的连接时，`keepalive`很有用。

开启`Keep-Alive`连接对性能有很大的影响：减少了打开和关闭连接所需的`CPU`和网络开销。

通过在`nginx`中启用`HTTP keepalive`，降低了`nginx`连接上游服务器的延迟，从而提高了性能，并减少了`nginx`耗尽临时端口的可能性。
`nginx`将重用现有的`TCP`连接,而不创建新的`TCP`,
这可以极大地减少繁忙服务器上`TIME_WAIT TCP`连接中的套接字数量(减少操作系统建立新连接的工作，减少网络上的数据包)

**注意：** 仅在`HTTP/1.1`时支持`Keep-Alive`连接。

> 配置样例

```nginx configuration
# Upstream context:
upstream backend {

  # Sets the maximum number of idle keepalive connections to upstream servers
  # that are preserved in the cache of each worker process.
  keepalive 16;

}

# Server/location contexts:
server {

  ...

  location / {

    # By default only talks HTTP/1 to the upstream,
    # keepalive is only enabled in HTTP/1.1:
    proxy_http_version 1.1;

    # Remove the Connection header if the client sends it,
    # it could be "close" to close a keepalive connection:
    proxy_set_header Connection "";

    ...

  }

}
```
