# ==================== 基础定义 ====================
%define realname nginx
%define orgnize wl
%define realver NGINX_VERSION
%define srcext tar.gz
%define opensslVersion openssl-OpenSSL_OPENSSL_VERSION
%define pcreVersion pcre-PCRE_VERSION
%define zlibVersion zlib-ZLIB_VERSION

# ==================== 通用信息 ====================
Name:           %{realname}
Version:        %{realver}
Release:        %{orgnize}%{?dist}
Summary:        Nginx is a web server software

License:        GPL
URL:            http://nginx.org

# ==================== 源码包 ====================
Source0:        %{realname}-%{realver}%{?extraver}.%{srcext}
Source1:        %{opensslVersion}.%{srcext}
Source2:        headers-more-nginx-module-0.37.tar.gz
Source3:        naxsi-0.56.tar.gz
Source4:        nginx_upstream_check_module-master.tar.gz
Source5:        ngx-fancyindex-master.tar.gz
Source6:        ngx_cache_purge-2.3.tar.gz
Source11:       nginx.logrotate
Source12:       nginx.conf
Source13:       conf
Source14:       nginx.service
Source15:       generate-ssl.sh
Source21:       %{pcreVersion}.%{srcext}
Source22:       %{zlibVersion}.%{srcext}
Source23:       LuaJIT-2.0.5.tar.gz
Source24:       lua-nginx-module-0.10.26.tar.gz
Source25:       ngx_devel_kit-0.3.3.tar.gz

# ==================== 依赖 ====================
Requires:       logrotate
BuildRequires:  gcc gcc-c++

# ==================== 描述 ====================
%description
nginx [engine x] is an HTTP and reverse proxy server

# ==================== 解压准备 ====================
#%prep
#%setup -q -n %{realname}-%{realver}%{?extraver} \
#    -a1 -a2 -a3 -a4 -a5 -a6 \
#    -a21 -a22 -a23 -a24 -a25
# ==================== 解压准备 ====================
# ==================== 解压准备 ====================
%prep
%setup -q -n %{realname}-%{realver}%{?extraver}

# 解压所有额外的 Source 文件
for source_file in \
    %{_sourcedir}/openssl-OpenSSL_1_1_1l.tar.gz \
    %{_sourcedir}/headers-more-nginx-module-0.37.tar.gz \
    %{_sourcedir}/naxsi-0.56.tar.gz \
    %{_sourcedir}/nginx_upstream_check_module-master.tar.gz \
    %{_sourcedir}/ngx-fancyindex-master.tar.gz \
    %{_sourcedir}/ngx_cache_purge-2.3.tar.gz \
    %{_sourcedir}/pcre-8.45.tar.gz \
    %{_sourcedir}/zlib-1.3.1.tar.gz \
    %{_sourcedir}/LuaJIT-2.0.5.tar.gz \
    %{_sourcedir}/lua-nginx-module-0.10.26.tar.gz \
    %{_sourcedir}/ngx_devel_kit-0.3.3.tar.gz
do
    if [ -f "$source_file" ]; then
        echo "Unpacking: $source_file"
        tar -xaf "$source_file" -C %{_builddir}/%{realname}-%{realver}%{?extraver}
    else
        echo "ERROR: $source_file not found"
        exit 1
    fi
done

# ==================== 编译 ====================
%build

# 调试：查看解压后的目录
ls -la %{_builddir}/%{realname}-%{realver}%{?extraver}/
ls -la %{_builddir}/%{realname}-%{realver}%{?extraver}/ | grep -E "(ngx_cache|headers-more|naxsi|fancyindex|upstream_check|ngx_devel_kit|lua)"

# 修复 ip_hash 模块的 IPv6 兼容性
sed -i "s;iphp->addrlen = 3;iphp->addrlen = 4;g" src/http/modules/ngx_http_upstream_ip_hash_module.c
sed -i "s;hash_pseudo_addr[3];hash_pseudo_addr[4];" src/http/modules/ngx_http_upstream_ip_hash_module.c

# Rocky Linux 8 特定配置
%if 0%{?rhel} == 8
# 确保使用系统 OpenSSL
export CFLAGS="-O2 -g -pipe"
%endif

# 配置编译选项
./configure \
    --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --modules-path=/usr/lib64/nginx/modules \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/run/nginx.lock \
    --http-client-body-temp-path=/var/cache/nginx/client_temp \
    --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
    --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
    --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
    --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
    --user=nginx \
    --group=nginx \
    --with-compat \
    --with-file-aio \
    --with-threads \
    --with-openssl=%{opensslVersion} \
    --with-pcre=%{pcreVersion} \
    --with-pcre-jit \
    --with-zlib=%{zlibVersion} \
    --add-module=ngx_cache_purge-2.3 \
    --add-module=headers-more-nginx-module-0.37 \
    --add-module=naxsi-0.56/naxsi_src \
    --add-module=ngx-fancyindex-master \
    --add-module=ngx_devel_kit-0.3.3 \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_mp4_module \
    --with-http_random_index_module \
    --with-http_realip_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-stream \
    --with-stream_realip_module \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module

# 并行编译
make %{?_smp_mflags}

# ==================== 安装 ====================
%install
# 安装二进制文件
%__make install DESTDIR=%{buildroot}

# 转换俄语文档编码
iconv -f koi8-r CHANGES.ru > c && %__mv -f c CHANGES.ru

# 创建必要目录
%__install -d %{buildroot}~/.vim

# 安装配置文件
%__install -D -m 444 %{S:11} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%__install -D -m 755 %{S:14} %{buildroot}%{_unitdir}/%{name}.service
%__install -D -m 755 %{S:15} %{buildroot}%{_sbindir}/generate-ssl.sh

# 复制辅助文件
%__cp -r -v %{_builddir}/%{realname}-%{realver}%{?extraver}/contrib/vim %{buildroot}/etc/nginx/
%__cp -r -v %{S:12} %{buildroot}/etc/nginx/nginx.conf
%__cp -r -v %{S:13} %{buildroot}/etc/nginx

# LuaJIT 相关（已注释，保留原样）
# %__cp -r -v %{_builddir}/%{realname}-%{realver}%{?extraver}/lj2 %{buildroot}/etc/nginx/

# ==================== 清理 ====================
%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# ==================== 文件清单 ====================
%files
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config %{_sbindir}/%{name}
%config %{_unitdir}/%{name}.service
%config %{_sbindir}/generate-ssl.sh
%doc
%{_sysconfdir}/nginx/*

# ==================== 安装后脚本 ====================
%post
# 创建 nginx 用户和组
groupadd nginx 2>/dev/null || true
useradd nginx -g nginx -s /sbin/nologin -M 2>/dev/null || true

# 创建必要目录
mkdir -p /var/log/nginx /var/cache/nginx /var/dump/nginx /usr/share/nginx

# 设置权限
chown -R nginx:nginx /var/log/nginx /var/cache/nginx /var/dump/nginx /usr/share/nginx /etc/nginx

# 配置 limits
cat >> /etc/security/limits.conf <<'EOF'
nginx soft nofile 65535
nginx hard nofile 65535
nginx soft nproc 65535
nginx hard nproc 65535
EOF

# 配置 logrotate 定时任务
(crontab -l 2>/dev/null | grep -v 'logrotate.d/nginx'; echo "0 0 * * * root /usr/sbin/logrotate -f /etc/logrotate.d/nginx") | \
    sort -u | crontab - 2>/dev/null || true

# 配置 vim 语法高亮
mkdir -p ~/.vim
cp -r /etc/nginx/vim ~/.vim/ 2>/dev/null || true
cat > ~/.vim/filetype.vim <<'EOF'
au BufRead,BufNewFile /etc/nginx/conf.d/*.conf set ft=nginx
EOF

# 生成 SSL 证书
mkdir -p /etc/nginx/ssl
cd /etc/nginx/ssl
%{_sbindir}/generate-ssl.sh 2>/dev/null || true

# ==================== 卸载前脚本 ====================
%preun
# 停止 nginx 服务
if [ -f /var/run/nginx.pid ]; then
    kill -15 `cat /var/run/nginx.pid` 2>/dev/null || true
fi

# ==================== 卸载后脚本 ====================
%postun
# 删除文件和目录
rm -rf /etc/nginx/ /var/log/nginx /var/cache/nginx /var/dump/nginx /usr/share/nginx 2>/dev/null || true

# 删除 nginx 用户
userdel nginx 2>/dev/null || true

# 清理 limits 配置
sed -i "/nginx soft nofile 65535/d" /etc/security/limits.conf
sed -i "/nginx hard nofile 65535/d" /etc/security/limits.conf
sed -i "/nginx soft nproc 65535/d" /etc/security/limits.conf
sed -i "/nginx hard nproc 65535/d" /etc/security/limits.conf

# 清理 crontab
(crontab -l 2>/dev/null | grep -v 'logrotate.d/nginx') | crontab - 2>/dev/null || true

# ==================== 变更日志 ====================
%changelog