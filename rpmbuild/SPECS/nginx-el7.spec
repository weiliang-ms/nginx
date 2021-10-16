%define realname nginx

%define orgnize wl

%define realver NGINX_VERSION

%define srcext tar.gz

%define opensslVersion openssl-OpenSSL_OPENSSL_VERSION

%define pcreVersion pcre-PCRE_VERSION

%define zlibVersion zlib-ZLIB_VERSION

# Common info

Name: %{realname}

Version: %{realver}

Release: %{orgnize}%{?dist}

Summary: Nginx is a web server software

License: GPL

URL: http://nginx.org

Source0: %{realname}-%{realver}%{?extraver}.%{srcext}

Source1: %{opensslVersion}.%{srcext}

Source2: headers-more-nginx-module-master.tar.gz

Source3: naxsi-0.56.tar.gz

Source4: nginx_upstream_check_module-master.tar.gz

Source5: ngx-fancyindex-master.tar.gz

Source6: ngx_cache_purge-2.3.tar.gz

Source11: nginx.logrotate

Source12: nginx.conf

Source13: conf

Source14: nginx.service

Source15: generate-ssl.sh

Source21: %{pcreVersion}.%{srcext}

Source22: %{zlibVersion}.%{srcext}

Source23: LuaJIT-2.0.5.tar.gz

Source24: lua-nginx-module-0.10.13.tar.gz

Source25: ngx_devel_kit-0.3.0.tar.gz

Requires: logrotate

BuildRequires: gcc gcc-c++

%description

nginx [engine x] is an HTTP and reverse proxy server

# Preparation step (unpackung and patching if necessary)

%prep
%setup -q -n %{realname}-%{realver}%{?extraver} -a1 -a2 -a3 -a4 -a5 -a6 -a21 -a22 -a23 -a24 -a25

%build
# lua
cd LuaJIT-2.0.5 && make -j $(nproc) && \
  make install PREFIX=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2
cd -

export LUAJIT_LIB=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2/lib
export LUAJIT_INC=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2/include/luajit-2.0

# ip_hash
set -e
sed -i "s;iphp->addrlen = 3;iphp->addrlen = 4;g" src/http/modules/ngx_http_upstream_ip_hash_module.c
sed -i "s;hash_pseudo_addr[3];hash_pseudo_addr[4];" src/http/modules/ngx_http_upstream_ip_hash_module.c
set +e

./configure --prefix=/etc/nginx \
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
    --add-module=headers-more-nginx-module-master \
    --add-module=naxsi-0.56/naxsi_src \
    --add-module=ngx-fancyindex-master \
    --add-module=ngx_devel_kit-0.3.0 \
    --add-module=lua-nginx-module-0.10.13 \
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_stub_status_module \
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

make -j $(nproc)

%install
%__make install DESTDIR=%{buildroot}
iconv -f koi8-r CHANGES.ru > c && %__mv -f c CHANGES.ru
%__install -d %{buildroot}~/.vim
%__install -D -m755 %{S:11} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%__install -D -m755 %{S:14} %{buildroot}%{_unitdir}/%{name}.service
%__install -D -m755 %{S:15} %{buildroot}%{_sbindir}/generate-ssl.sh
%__cp -r -v %{_builddir}/%{realname}-%{realver}%{?extraver}/lj2 %{buildroot}/etc/nginx/
%__cp -r -v %{_builddir}/%{realname}-%{realver}%{?extraver}/contrib/vim %{buildroot}/etc/nginx/
%__cp -r -v %{S:12} %{buildroot}/etc/nginx/nginx.conf
%__cp -r -v %{S:13} %{buildroot}/etc/nginx
%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config %{_sbindir}/%{name}
%config %{_unitdir}/%{name}.service
%config %{_sbindir}/generate-ssl.sh
%doc
%{_sysconfdir}/nginx/*

%post

groupadd nginx
useradd nginx -g nginx -s /sbin/nologin -M

mkdir -p /var/log/nginx /var/cache/nginx /var/dump/nginx /usr/share/nginx
chown nginx:nginx -R /var/log/nginx
chown nginx:nginx -R /var/cache/nginx
chown nginx:nginx -R /var/dump/nginx
chown nginx:nginx -R /usr/share/nginx
chown nginx:nginx -R /etc/nginx

echo "nginx soft nofile 65535" >> /etc/security/limits.conf
echo "nginx hard nofile 65535" >> /etc/security/limits.conf
echo "nginx soft nproc 65535" >> /etc/security/limits.conf
echo "nginx hard nproc 65535" >> /etc/security/limits.conf

# logratate crontab
crontab -l | grep -v '#' > /tmp/file1
echo "0 0 * * * root bash /usr/sbin/logrotate -f /etc/logrotate.d/nginx" >> /tmp/file1 && awk ' !x[$0]++{print > "/tmp/file1"}' /tmp/file1
crontab /tmp/file1

mkdir -p ~/.vim
cp -r -v /etc/nginx/vim ~/.vim/
cat > ~/.vim/filetype.vim <<EOF
au BufRead,BufNewFile /etc/nginx/conf.d/*.conf set ft=nginx
EOF

chmod +x /etc/nginx/lj2/lib/*

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/etc/nginx/lj2/lib
\cp /etc/nginx/lj2/lib/libluajit-5.1.so.2 /lib/
ldconfig

mkdir -p /etc/nginx/ssl
cd /etc/nginx/ssl
%{_sbindir}/generate-ssl.sh

%postun

if [ -f /var/run/nginx.pid ];then
    kill -15 `cat /var/run/nginx.pid`
fi

rm -rf /etc/nginx/
rm -rf /var/log/nginx /var/cache/nginx /var/dump/nginx /usr/share/nginx
userdel nginx
sed -i "/nginx soft nofile 655350/d" /etc/security/limits.conf
sed -i "/nginx hard nofile 655350/d" /etc/security/limits.conf
sed -i "/nginx soft nproc 65535/d" /etc/security/limits.conf
sed -i "/nginx hard nproc 65535/d" /etc/security/limits.conf

crontab -l | grep -v 'nginx' > /tmp/file1
crontab /tmp/file1
%changelog