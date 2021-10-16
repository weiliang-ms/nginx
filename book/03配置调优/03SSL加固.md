### SSL会话缓存

默认情况下，`内置`会话缓存功能是不合理的，因为该缓存只能被一个`worker`进程使用，并且可能导致内存碎片化。

> 使用`ssl_session_cache`指令处理会话缓存可以降低`NGINX`服务器的`CPU`开销。

从客户端角度来看，通过对`ssl`会话缓存可以提高系统性能。其原理主要是：消除了每次发出请求时都需要进行新的(且耗时的)`SSL`握手的需要。

> `ssl_session_cache`值该怎么设？

当启用`ssl_session_cache`时，通过`SSL`保持的连接，性能会大大提高。

建议`ssl_session_cache`值设为`10M`(`1MB`共享缓存可以容纳大约`4000`个会话)。
共享的缓存在所有`worker`进程之间共享(同名的缓存可以在多个虚拟服务器中使用，但不跨主机因为基于宿主机内存)。

> `ssl_session_timeout`参数设置

对于`TLSv1.2`，会话的缓存时间不应超过24小时(这是最大时间)。

通常，`TLS`会话不应该被恢复，除非客户端和服务器都同意，并且如果任何一方怀疑会话可能已被泄露，或者证书可能已过期或已被吊销，则应该强制执行完全握手。

但是一段时间以前，我发现`ssl_session_timeout`设置较短的时间(例如15分钟)可以防止被广告商滥用，如谷歌和`Facebook`，针对这这种情况是有意义的。

建议值设置为
```nginx configuration
ssl_session_timeout 4h;
```

> `ssl_buffer_size`参数设置


### 开启OCSP Stapling

[Enable OCSP Stapling](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-23)

与`OCSP`不同，在`OCSP Stapling`机制中，用户的浏览器不会直接访问证书的颁发者进行证书校验，而是由应用服务器定期访问颁发者进行证书校验。

`OCSP Stapling`扩展配置是为了更好的性能(旨在减少OCSP验证的成本;提高浏览器与应用服务器的通信性能，
并允许在访问应用程序时检索有关证书有效性的信息)，用户隐私仍然得到维护。`OCSP Stapling`只是一种优化，即使他不起作用，也不会中断程序。

在没有实现`OCSP Stapling`扩展的情况下使用`OCSP`，会增加丢失用户隐私的风险，
以及由于无法验证证书的有效性而对应用程序的可用性造成负面影响的风险。

`OCSP Stapling`在`TLS`证书状态请求(RFC 6066 -证书状态请求)扩展(`Stapling`)中定义了`OCSP`响应。
在这种情况下，服务器发送`OCSP`响应作为`TLS`扩展的一部分，因此客户端不需要在`OCSP URL`上检查它(为客户端节省了撤销检查时间)。

`nginx`提供了几个需要记住的选项。
例如:它从`ssl_trusted_certificate`所指向的证书文件生成列表(这些证书的列表将不会发送到客户端)。
您需要发送这个列表或关闭`ssl_verify_client`。
当`ssl_certificate`语句已经提供了完整的证书链(只有中级证书，没有根CA，而且必须不包括站点证书)时，
此步骤是可选的。如果只使用证书(而不是`CA`的部分)，则需要`ssl_trusted_certificate`。



