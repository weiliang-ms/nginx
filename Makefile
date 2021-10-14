NGINX_VERSION:=1.20.1
OPENSSL_VERSION:=1_1_1l
PCRE_VERSION:=8.45
ZLIB_VERSION:=1.2.11

RESOURCE_DIR:=rpmbuild/SOURCES
SPECS_DIR:=rpmbuild/SPECS

NGINX_DOWNLOAD_URL:=https://nginx.org/download
OPENSSL_DOWNLOAD_URL:=https://github.com/openssl/openssl/archive/refs/tags
PCRE_DOWNLOAD_URL:=http://ftp.pcre.org/pub/pcre
ZLIB_DOWNLOAD_URL:=http://www.zlib.net

download:
	pwd
	curl -L --connect-timeout 10 -m 20 ${NGINX_DOWNLOAD_URL}/nginx-${NGINX_VERSION}.tar.gz \
		-o ${RESOURCE_DIR}/nginx-${NGINX_VERSION}.tar.gz

	curl -L --connect-timeout 10 -m 20 ${OPENSSL_DOWNLOAD_URL}/OpenSSL_${OPENSSL_VERSION}.tar.gz \
    		-o ${RESOURCE_DIR}/openssl-OpenSSL_${OPENSSL_VERSION}.tar.gz

	curl -L --connect-timeout 10 -m 20 ${PCRE_DOWNLOAD_URL}/pcre-${PCRE_VERSION}.tar.gz \
			-o ${RESOURCE_DIR}/pcre-${PCRE_VERSION}.tar.gz

	curl -L --connect-timeout 10 -m 20 ${ZLIB_DOWNLOAD_URL}/zlib-${ZLIB_VERSION}.tar.gz \
			-o ${RESOURCE_DIR}/zlib-${ZLIB_VERSION}.tar.gz

replace:
	pwd
	sed -i "s#NGINX_VERSION#${NGINX_VERSION}#" ${SPECS_DIR}/nginx-el7.spec
	sed -i "s#OPENSSL_VERSION#${OPENSSL_VERSION}#" ${SPECS_DIR}/nginx-el7.spec
	sed -i "s#PCRE_VERSION#${PCRE_VERSION}#" ${SPECS_DIR}/nginx-el7.spec
	sed -i "s#ZLIB_VERSION#${ZLIB_VERSION}#" ${SPECS_DIR}/nginx-el7.spec

	sed -i "s#NGINX_VERSION#${NGINX_VERSION}#" ${SPECS_DIR}/nginx-el6.spec
	sed -i "s#OPENSSL_VERSION#${OPENSSL_VERSION}#" ${SPECS_DIR}/nginx-el6.spec
	sed -i "s#PCRE_VERSION#${PCRE_VERSION}#" ${SPECS_DIR}/nginx-el6.spec
	sed -i "s#ZLIB_VERSION#${ZLIB_VERSION}#" ${SPECS_DIR}/nginx-el6.spec
	cat ${SPECS_DIR}/nginx-el7.spec

all: download replace