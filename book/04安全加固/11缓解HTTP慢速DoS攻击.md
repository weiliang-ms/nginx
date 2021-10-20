### 缓解HTTP慢速DoS攻击

[Mitigating Slow HTTP DoS attacks](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-64)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

您可以关闭不太频繁写入数据的连接 ，过长的`keepalive`时间将降低服务器接受新连接的能力。

在我看来，`2-3`秒的`keepalive_timeout`对于大多数人来说已经足够解析`HTML/CSS`和检索所需的图像、图标，
设置过高`keepalive_timeout`将导致资源(主要是内存)的浪费，因为即使没有流量，连接也将保持打开状态，这对系统性能可能产生明显影响。

并且`send_timeout`最好设置的小些，这样一来`web`服务器将迅速关闭连接，释放资源，供新连接使用，从而提供系统吞吐。

当然超时配置还需根据实际情况进行配置，部分请求可能需要较长的时间接收响应（这部分请求最好在`location`上下文单独配置超时时间）。

> 配置样例(参考值)

```nginx configuration
client_body_timeout 10s;    # default: 60s
client_header_timeout 10s;  # default: 60s
keepalive_timeout 5s 5s;    # default: 75s
send_timeout 10s;           # default: 60s
```
