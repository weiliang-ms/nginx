## worker调优

[原文地址](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#beginner-adjust-worker-processes)

`worker_processes`是`nginx`的核心指令。

该指令用于声明：`nginx`启动时，将会启动多少个`worker`进程，当`nginx`运行在`cpu`密集型的宿主机上很有用。

最简单的方式就是配置为: `auto`。当然也可以根据高并发情况下的最大吞吐量调整此值。
从合理利用计算资源的角度来看，应该根据可用内核数、磁盘、网络子系统、服务器负载等将该值更改为最佳值。

### 应该配置多少个`worker`进程？

首先，对`nginx`进行压力测试，测试当配置一个`worker`进程时，负载情况。

然后，依次增加`worker`数量，继续观测负载情况，直到服务器资源达到真正饱和的程度。

此时，`worker`数量便有了对应的值。

> 尽可能为系统预留一部分`cpu`计算资源

对于高负载代理服务器(也包括独立服务器)，更合理的值应为：`worker num = ALL_CORES - 1` (或更多)

因为如果你在同一台服务器上运行`NGINX`和其他关键服务，通过预留一部分`CPU核`给其他关键服务或系统服务，
避免`nginx`高负载运行情况下对系统/其他关系服务产生严重影响。

> 经验值

当`nginx`在处理请求时，很大一部分时间用于处理`I/O`，那么此时需要增加`worker`进程数量。

### 官方建议

> `nginx`官方文档说明如下:

当你不知道该如何设置这个参数时，将其设置为可用`CPU`核的数量将是一个很好的选择。

即每个`CPU`内核运行一个`worker`进程，这种方式能最有效地使用硬件资源。

```shell
# 推荐方式:
worker_processes auto;

# 可选方式:
# VCPU = 4 ，worker_processes = VCPU - 1
# VCPU -> grep "processor" /proc/cpuinfo | wc -l
worker_processes 3;
```