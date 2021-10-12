NGINX_VERSION:=1.20.1
OPENSSL_VERSION:=1_1_1l

RESOURCE_DIR:=rpmbuild/SOURCES
SPECS_DIR:=rpmbuild/SPECS

NGINX_DOWNLOAD_URL:=https://nginx.org/download
OPENSSL_DOWNLOAD_URL:=https://github.com/openssl/openssl/archive/refs/tags

download:
	pwd
	curl -L --connect-timeout 10 -m 20 ${NGINX_DOWNLOAD_URL}/nginx-${NGINX_VERSION}.tar.gz \
		-o ${RESOURCE_DIR}/nginx-${NGINX_VERSION}.tar.gz

	curl -L --connect-timeout 10 -m 20 ${OPENSSL_DOWNLOAD_URL}/OpenSSL_${OPENSSL_VERSION}.tar.gz \
    		-o ${RESOURCE_DIR}/openssl-OpenSSL_${OPENSSL_VERSION}.tar.gz

	pwd
	ls ${RESOURCE_DIR}

replace:
	pwd
	sed -i "s#NGINX_VERSION#${NGINX_VERSION}#" ${SPECS_DIR}/nginx-el7.spec
	sed -i "s#OPENSSL_VERSION#${OPENSSL_VERSION}#" ${SPECS_DIR}/nginx-el7.spec
	cat ${SPECS_DIR}/nginx-el7.spec

build:
	yum install -y rpm-build dos2unix
	pwd
	ls ${RESOURCE_DIR}
	rpmbuild -ba rpmbuild/SPECS/nginx-el7.spec

all: download replace build