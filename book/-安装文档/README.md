## 安装部署

> 下载最新`release`版本

- [release](https://github.com/weiliang-ms/nginx/releases)

### CentOS7

> 安装

```shell
rpm -ivh nginx-*-wl.el7.x86_64.rpm
```

> 关闭`selinux`

```shell
setenforce 0
sed -i "s#SELINUX=enforcing#SELINUX=disabled#g" /etc/selinux/config
```

> 启动

```shell
systemctl daemon-reload
systemctl enable nginx --now
```

> 查看状态

```shell
systemctl status nginx
```