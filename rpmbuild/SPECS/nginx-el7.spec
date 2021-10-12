%define realname nginx

%define orgnize wl

%define realver NGINX_VERSION

%define srcext tar.gz

%define opensslVersion openssl-OpenSSL_OPENSSL_VERSION

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

#Source12: nginx.conf

Source13: conf

Source14: nginx

Source21: pcre-8.44.tar.gz

Source22: zlib-1.2.11.tar.gz

Source23: LuaJIT-2.0.5.tar.gz

Source24: lua-nginx-module-0.10.13.tar.gz

Source25: ngx_devel_kit-0.3.0.tar.gz

Requires: logrotate

#BuildRequires: gcc zlib-devel pcre-devel

%description

nginx [engine x] is an HTTP and reverse proxy server

# Preparation step (unpackung and patching if necessary)

%prep
%setup -n modules -a1 -a2 -a3 -a4 -a5 -a6 -a21 -a22 -a23 -a24 -a25
%setup -T -b 0

%build

# lua
cd modules/LuaJIT-2.0.5 && make -j $(nproc) && \
  make install PREFIX=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2
cd -

export LUAJIT_LIB=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2/lib
export LUAJIT_INC=%{_builddir}/%{realname}-%{realver}%{?extraver}/lj2/include/luajit-2.0

./configure --prefix=/opt/nginx --with-stream \
        --pid-path=/var/run/nginx.pid \
        --sbin-path=%{_sbindir}/%{name}
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

%install
%__make install DESTDIR=%{buildroot}
iconv -f koi8-r CHANGES.ru > c && %__mv -f c CHANGES.ru
%__install -d %{buildroot}~/.vim
%__install -D -m755 %{S:11} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%__install -D -m755 %{S:14} %{buildroot}%{_sysconfdir}/init.d/%{name}
%__cp -r -v %{_builddir}/%{realname}-%{realver}%{?extraver}/lj2 %{buildroot}/opt/nginx/
%__cp -r -v %{_builddir}/%{realname}-%{realver}%{?extraver}/contrib/vim %{buildroot}/opt/nginx/
%__cp -r -v %{S:13}/* %{buildroot}/opt/nginx/conf/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/init.d/%{name}
%config %{_sbindir}/%{name}
%doc
/opt/nginx/*

%post

chkconfig nginx on

echo "* soft nofile 655350" >> /etc/security/limits.conf

echo "* hard nofile 655350" >> /etc/security/limits.conf

echo "* soft nproc 65535" >> /etc/security/limits.conf

echo "* hard nproc 65535" >> /etc/security/limits.conf

#sed -i '/\/etc\/logrotate.d\/nginx/d' /etc/crontab
#echo "0 0 * * * root bash /usr/sbin/logrotate -f /etc/logrotate.d/nginx" >> /etc/crontab
mkdir -p ~/.vim
cp -r -v /opt/nginx/vim ~/.vim/
cat > ~/.vim/filetype.vim <<EOF
au BufRead,BufNewFile /opt/nginx/conf/conf.d/*.conf set ft=nginx
EOF

chmod +x /opt/nginx/lj2/lib/*

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nginx/lj2/lib
\cp /opt/nginx/lj2/lib/libluajit-5.1.so.2 /lib/
ldconfig

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

%postun

rm -f /opt/nginx/

sed -i "/* soft nofile 655350/d" /etc/security/limits.conf
sed -i "/* hard nofile 655350/d" /etc/security/limits.conf
sed -i "/* soft nproc 65535/d" /etc/security/limits.conf
sed -i "/* hard nproc 65535/d" /etc/security/limits.conf

%changelog