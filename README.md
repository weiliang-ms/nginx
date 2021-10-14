![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/weiliang-ms/nginx-rpm/build-el7?style=flat-square)
![GitHub all releases](https://img.shields.io/github/downloads/weiliang-ms/nginx-rpm/total?style=flat-square)
![GitHub](https://img.shields.io/github/license/weiliang-ms/easyctl?style=flat-square)

## 适用场景

- 一键式安装`nginx`，无需安装其依赖（如zlib-devel|pcre-devel|openssl-devel）
- 安全可控：可随时更新依赖包版本、模块包版本、`nginx`版本，降低软件漏洞所带来的风险

[nginx使用文档地址](https://weiliang-ms.github.io/nginx/)

## 优势

内置如下模块/特性:

- 内嵌模块
  - [修改http头模块](https://github.com/openresty/headers-more-nginx-module)
  - [waf模块](https://github.com/loveshell/ngx_lua_waf)
- 特性列表
  - [日志文件轮转](https://linux.cn/article-4126-1.html)
  - [配置文件语法高亮](https://www.cnblogs.com/manastudent/p/12936546.html)
  - [ip_hash支持基于主机号hash](https://blog.csdn.net/yswKnight/article/details/107180893)
  - [开启nginx dump](https://github.com/trimstray/nginx-admins-handbook/blob/master/doc/RULES.md#beginner-use-core-dumps-to-figure-out-why-nginx-keep-crashing)
  - 内置ssl生成工具
- 使用样例
  - [x] [ssl配置](book/02配置样例/01ssl配置样例.md)
- 调优列表
  - [x] [worker数量](book/03配置调优/01worker数量调优.md)
  - [ ] [使用HTTP2](book/03配置调优/02使用HTTP2.md)

### 构建介质

- [pcre](https://sourceforge.net/projects/pcre/files/pcre/8.45/pcre-8.45.tar.gz/download)