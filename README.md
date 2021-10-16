![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/weiliang-ms/nginx-rpm/build-el7?style=flat-square)
![GitHub all releases](https://img.shields.io/github/downloads/weiliang-ms/nginx-rpm/total?style=flat-square)
![GitHub](https://img.shields.io/github/license/weiliang-ms/easyctl?style=flat-square)

## 适用场景

- 一键式安装`nginx`，无需安装其依赖（如zlib-devel|pcre-devel|openssl-devel）
- 安全可控：可随时更新依赖包版本、模块包版本、`nginx`版本，降低软件漏洞所带来的风险

[nginx使用文档地址](https://weiliang-ms.github.io/nginx/)

## 优势

- [ ] 代表需要手动开启
- [x] 代表内置开启

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
  - [ ] [https加固](book/03配置调优/03SSL加固.md)
  - [ ] [使用server_name代替if指令判断domain](book/03配置调优/04使用server_name代替if指令判断domain.md)
  - [ ] [使用$request_uri代替正则](book/03配置调优/05使用$request_uri代替正则.md)
  - [ ] [使用try_files指令来确保文件存在](book/03配置调优/06使用try_files指令来确保文件存在.md)
  - [ ] [使用return代替rewrite做重定向](book/03配置调优/07使用return代替rewrite做重定向.md)
  - [ ] [pcre开启JIT调优](book/03配置调优/08启用PCRE-JIT以加速正则表达式的处理.md)
  - [ ] [upstream开启keepalive](book/03配置调优/09upstream开启keepalive.md)
  - [ ] [尽可能精准配置location](book/03配置调优/10尽可能精准配置location.md)
- 加固列表
  - [x] 安装最新版`nginx`
  - [x] 使用最新版本`openssl`
  - [x] [使用非特权用户运行nginx](book/04安全加固/02使用非特权用户运行nginx.md)
  - [x] [隐藏版本信息](book/04安全加固/04隐藏nginx版本信息.md)
  - [ ] [保护敏感资源](book/04安全加固/03保护敏感资源.md)
  - [ ] ssl加固(TODO)
  

## TODO

- [ ] 自定义异常页
- [ ] lua块
- [ ] waf功能
- [ ] 全局黑名单
- [ ] debug

### 构建介质

- [pcre](https://sourceforge.net/projects/pcre/files/pcre/8.45/pcre-8.45.tar.gz/download)