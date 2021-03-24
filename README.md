![GitHub](https://img.shields.io/github/license/weiliang-ms/nginx-rpm)

- [nginx rpm包](#nginx-rpm%E5%8C%85)
  - [适用场景](#%E9%80%82%E7%94%A8%E5%9C%BA%E6%99%AF)
  - [构建](#%E6%9E%84%E5%BB%BA)
  - [rpmbuild解析](#rpmbuild%E8%A7%A3%E6%9E%90)
    - [目录结构说明](#%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84%E8%AF%B4%E6%98%8E)
    - [定义变量](#%E5%AE%9A%E4%B9%89%E5%8F%98%E9%87%8F)
    - [软件信息](#%E8%BD%AF%E4%BB%B6%E4%BF%A1%E6%81%AF)
    - [声明构建介质](#%E5%A3%B0%E6%98%8E%E6%9E%84%E5%BB%BA%E4%BB%8B%E8%B4%A8)
    - [声明运行时依赖](#%E5%A3%B0%E6%98%8E%E8%BF%90%E8%A1%8C%E6%97%B6%E4%BE%9D%E8%B5%96)
    - [prep准备阶段](#prep%E5%87%86%E5%A4%87%E9%98%B6%E6%AE%B5)
    - [build构建阶段](#build%E6%9E%84%E5%BB%BA%E9%98%B6%E6%AE%B5)
    - [install安装阶段](#install%E5%AE%89%E8%A3%85%E9%98%B6%E6%AE%B5)
    - [clean清理阶段](#clean%E6%B8%85%E7%90%86%E9%98%B6%E6%AE%B5)
    - [rpm包制作阶段](#rpm%E5%8C%85%E5%88%B6%E4%BD%9C%E9%98%B6%E6%AE%B5)
    - [post阶段](#post%E9%98%B6%E6%AE%B5)
    - [postun阶段](#postun%E9%98%B6%E6%AE%B5)
# nginx rpm包
## 适用场景

- 一键式安装`nginx`，无需安装其依赖（如zlib-devel|pcre-devel|openssl-devel）
- 安全可控：可随时更新依赖包版本、模块包版本、`nginx`版本，降低软件漏洞所带来的风险

## 构建

`CenOS7`下，执行

    yum install -y rpm-build dos2unix
    git clone https://github.com/weiliang-ms/nginx-rpm.git
    dos2unix nginx-rpm/rpmbuild/SPECS/nginx.spec
    rpmbuild -ba nginx-rpm/rpmbuild/SPECS/nginx.spec
    
## rpmbuild解析

### 目录结构说明


| 目录名 | 说明 | macros中的宏名 |
| :-----:| :----: | :----: |
| BUILD | 编译rpm包的临时目录 | %_builddir |
| BUILDROOT | 编译后生成的软件临时安装目录 | %_buildrootdir |
| RPMS | 最终生成的可安装rpm包的所在目录 | %_rpmdir |
| SOURCES | 所有源代码和补丁文件的存放目录 | %_sourcedir |
| SPECS | 存放SPEC文件的目录 | %_specdir |
| SRPMS | 软件最终的rpm源码格式存放路径 | %_srcrpmdir |

### 定义变量


- `%define realname nginx` 定义软件名称为`nginx`

- `%define orgnize wl` 定义所属组织`wl`

- `%define realver 1.18.0` 定义软件版本号

- `%define srcext tar.gz` 定义软件源码包后缀

- `%define opensslVersion openssl-1.1.1j` 定义openssl版本

### 软件信息

- `Name: %{realname}`

- `Version: %{realver}` 

- `Release: %{orgnize}%{?dist}`

- `Summary: Nginx is a web server software` 描述

- `License: GPL` 许可协议

- `URL: http://nginx.org` 官网

### 声明构建介质

存放目录为`rpmbuild/SOURCES`

    Source0: %{realname}-%{realver}%{?extraver}.%{srcext}
    
    Source1: %{opensslVersion}.tar.gz
    
    Source2: headers-more-nginx-module-master.tar.gz
    
    Source3: naxsi-0.56.tar.gz
    
    Source4: nginx_upstream_check_module-master.tar.gz
    
    Source5: ngx-fancyindex-master.tar.gz
    
    Source6: ngx_cache_purge-2.3.tar.gz
    
    Source11: nginx.logrotate
    
    #Source12: nginx.conf
    
    Source13: conf
    
    Source14: nginx
    
    Source21: pcre-8.44.tar.gz
    
    Source22: zlib-1.2.11.tar.gz
    
    Source23: LuaJIT-2.0.5.tar.gz
    
    Source24: lua-nginx-module-0.10.13.tar.gz
    
    Source25: ngx_devel_kit-0.3.0.tar.gz

### 声明运行时依赖

编译好的`rpm`软件在其他机器上安装时，需要依赖的其他软件包，也以逗号分隔，有版本需求的可以

    Requires:      logrotate
    
### prep准备阶段

- `%prep` 准备阶段,将`%_sourcedir`(SOURCES)目录下的源代码解压到`%_builddir`(BUILD)目录下。如果有补丁的需要在这个阶段进行打补丁的操作
- `%setup -q` 解压并抑止不必要的输出
- `-n` 切换至指定目录
- `-a number` 在切换目录后，只解压指定序号的`Source`文件（例如 `-a1` 表示`Source1`）

解压`%{realname}-%{realver}%{?extraver}`并将`Source1`、`Source2`、`Source3`、`Source4`、`Source5`、`Source6`、`Source21`、`Source22`、`Source23`、`Source24`、`Source25`
解压至`%{realname}-%{realver}`

    %prep
    %setup -q -n %{realname}-%{realver}%{?extraver} -a1 -a2 -a3 -a4 -a5 -a6 -a21 -a22 -a23 -a24 -a25
    
### build构建阶段


构建阶段：在`%_builddir`（BUILD）目录下执行源码包的编译。一般是执行`./configure`和`make`指令

    %build
    
构建`lua`依赖

    # lua
    cd LuaJIT-2.0.5 && make -j $(nproc) && \
      make install PREFIX=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2
    cd ../
    
    export LUAJIT_LIB=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2/lib
    export LUAJIT_INC=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2/include/luajit-2.0
    
编译构建`nginx`

    ./configure --prefix=/opt/nginx --with-stream \
            --pid-path=/var/run/nginx.pid \
            --with-openssl=./%{opensslVersion} \
            --with-pcre=./pcre-8.44 \
            --with-zlib=./zlib-1.2.11 \
            --with-stream_ssl_preread_module --with-stream_ssl_module \
            --with-http_stub_status_module --with-http_ssl_module \
            --with-http_gzip_static_module \
            --add-module=./ngx_cache_purge-2.3 \
            --add-module=./headers-more-nginx-module-master \
            --add-module=./naxsi-0.56/naxsi_src \
            --add-module=./ngx-fancyindex-master \
            --add-module=./ngx_devel_kit-0.3.0 \
            --add-module=./lua-nginx-module-0.10.13
    make -j $(nproc)

### install安装阶段

安装阶段，将需要打包到`rpm`软件包里的文件从`%_builddir`下拷贝到`%_buildrootdir`（`%{buildroot}`）目录下。当用户最终用`rpm -ivh name-version.rpm`安装软件包时，这些文件会安装到用户系统中相应的目录里

    %install
    
安装`nginx`至`%{buildroot}`

    %__make install DESTDIR=%{buildroot}
    iconv -f koi8-r CHANGES.ru > c && %__mv -f c CHANGES.ru
    
创建`%{buildroot}~/.vim`目录
    
    %__install -d %{buildroot}~/.vim
    
拷贝`rpmbuild/SOURCES/nginx.logrotate`文件至`%{buildroot}/etc/logrotate.d/nginx.logrotate`   
    
    %__install -D -m755 %{S:11} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
    
拷贝`rpmbuild/SOURCES/nginx`文件至`%{buildroot}/etc/init.d/nginx`   
    
    %__install -D -m755 %{S:14} %{buildroot}%{_sysconfdir}/init.d/%{name}

拷贝`rpmbuild/BUILD/nginx-wl-1.18.0/contrib/lj2`目录至`%{buildroot}/opt/nginx/`    
    
    %__cp -r -v %{_builddir}/%{realname}-%{realver}%{?extraver}/lj2 %{buildroot}/opt/nginx/
   
拷贝`rpmbuild/BUILD/nginx-wl-1.18.0/contrib/vim`目录至`%{buildroot}/opt/nginx/`
   
    %__cp -r -v %{_builddir}/%{realname}-%{realver}%{?extraver}/contrib/vim %{buildroot}/opt/nginx/
   
拷贝`rpmbuild/SOURCES/conf/*`文件至`%{buildroot}/opt/nginx/conf/`
   
    %__cp -r -v %{S:13}/* %{buildroot}/opt/nginx/conf/

### clean清理阶段

清理阶段：编译后的清理工作，这里可以执行`make clean`以及清空`%_buildroot`目录等

    %clean
    [ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
    
### rpm包制作阶段

这个阶段必须引出下面一个叫做`%files`的阶段。它主要用来说明会将%`{buildroot}`目录下的哪些文件和目录最终打包到rpm包里
    
`%config`(noreplace)将保持旧文件 并将新文件安装为`.rpmnew`

    %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
    %config(noreplace) %{_sysconfdir}/init.d/%{name}
    %doc
    /opt/nginx/*
    
### post阶段

安装或者升级软件前要做的事情，比如停止服务、备份相关文件等都在这里做

    %post
    
配置开机自启动
    
    chkconfig nginx on
    
配置系统描述符
    
    echo "* soft nofile 655350" >> /etc/security/limits.conf
    
    echo "* hard nofile 655350" >> /etc/security/limits.conf
    
    echo "* soft nproc 65535" >> /etc/security/limits.conf
    
    echo "* hard nproc 65535" >> /etc/security/limits.conf
    
配置`nginx vim`语法高亮
    
    mkdir -p ~/.vim
    cp -r -v /opt/nginx/vim ~/.vim/
    cat > ~/.vim/filetype.vim <<EOF
    au BufRead,BufNewFile /opt/nginx/conf/conf.d/*.conf set ft=nginx
    EOF
    
配置动态库

    chmod +x /opt/nginx/lj2/lib/*
    
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nginx/lj2/lib
    \cp /opt/nginx/lj2/lib/libluajit-5.1.so.2 /lib/
    ldconfig
    
生成`ssl`

    mkdir -p /opt/nginx/ssl
    
    cd /opt/nginx/ssl
    
    # 域名
    export domain=www.nginx.com
    
    # IP地址（可选）
    export address=192.168.1.11
    
    # 国家
    export contryName=CN
    
    # 省/州/邦
    export stateName=Liaoning
    
    # 地方/城市名
    export locationName=Shenyang
    
    # 组织/公司名称
    export organizationName=example
    
    # 组织/公司部门名称
    export sectionName=develop
    
    echo "Getting Certificate Authority..."
    openssl genrsa -out ca.key 4096
    openssl req -x509 -new -nodes -sha512 -days 3650 \
      -subj "/C=$contryName/ST=$stateName/L=$locationName/O=$organizationNaem/OU=$sectionName/CN=$domain" \
      -key ca.key \
      -out ca.crt
    
    echo "Create your own Private Key..."
    openssl genrsa -out nginx.key 4096
    
    echo "Generate a Certificate Signing Request..."
    openssl req -sha512 -new \
      -subj "/C=$contryName/ST=$stateName/L=$locationName/O=$organizationNaem/OU=$sectionName/CN=$domain" \
      -key nginx.key \
      -out $domain.csr
    
    echo "Generate the certificate of your registry host..."
    cat > v3.ext <<-EOF
    authorityKeyIdentifier=keyid,issuer
    basicConstraints=CA:FALSE
    keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
    extendedKeyUsage = serverAuth
    subjectAltName = @alt_names
    [alt_names]
    DNS.1=$domain
    DNS.2=hostname
    IP.1=$address
    EOF
    openssl x509 -req -sha512 -days 3650 \
      -extfile v3.ext \
      -CA ca.crt -CAkey ca.key -CAcreateserial \
      -in $domain.csr \
      -out nginx.crt
    
    echo "Convert server nginx.crt to $domain.cert..."
    openssl x509 -inform PEM -in nginx.crt -out $domain.cert
    
    echo "merge the intermediate certificate with your own certificate to create a certificate bundle..."
    cp nginx.crt /etc/pki/ca-trust/source/anchors/nginx.crt
    update-ca-trust
    
    echo "successful..."
    
### postun阶段

卸载软件之后要做的事情，比如删除备份、配置文件等

    rm -f /opt/nginx/
    
    sed -i "/* soft nofile 655350/d" /etc/security/limits.conf
    
    sed -i "/* hard nofile 655350/d" /etc/security/limits.conf
    
    sed -i "/* soft nproc 65535/d" /etc/security/limits.conf
    
    sed -i "/* hard nproc 65535/d" /etc/security/limits.conf