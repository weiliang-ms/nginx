### 使用非特权用户运行nginx
[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#rationale-35)
- [更多nginx文档](https://weiliang-ms.github.io/nginx/)
- [更多linux相关文档](https://weiliang-ms.github.io/wl-awesome/)

`linux`下一个很重要的通用原则: 程序只应拥有完成其工作所需的最小权限。这样，如果程序坏了，它对系统的损害是有限的。

仅仅通过更改进程所有者名称，在安全性方面并没有真正的区别。
而在安全方面，最小特权原则规定：进程实体在给定系统中实现其目标所必需的权限之外，不应该被授予更多的权限。这样，只有`master`进程作为`root`进程运行。

```shell
[root@localhost ~]# ps -ef|grep nginx
root       1049      1  0 00:02 ?        00:00:00 nginx: master process /usr/sbin/nginx
nginx      1051   1049  0 00:02 ?        00:00:00 nginx: worker process
nginx      1052   1049  0 00:02 ?        00:00:00 nginx: cache manager process
nginx      1053   1049  0 00:02 ?        00:00:00 nginx: cache loader process
root       1317   1297  0 00:03 pts/0    00:00:00 grep --color=auto nginx
```

如果您使用这个仓库:[nginx](https://github.com/weiliang-ms/nginx) 的安装包进行安装，关于最小权限的配置已配置完毕：

- `master`进程运行`user`: `root` 
- `worker`进程运行`user`: `nginx`
- 目录权限
  - `/var/log/nginx`: 日志目录(nginx:nginx)
  - `/var/cache/nginx`: 缓存目录(nginx:nginx)
  - `/var/dump/nginx`: `dump`目录(nginx:nginx)
  - `/etc/nginx`: 配置目录(nginx:nginx)
  - `/usr/share/nginx`: 静态文件目录(nginx:nginx)
