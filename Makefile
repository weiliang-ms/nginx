NGINX_VERSION:="1.20.1"

RESOURCE_DIR:="rpmbuild/SOURCES"
SPECS_DIR:="rpmbuild/SPECS"

NGINX_DOWNLOAD_URL:="https://nginx.org/download/nginx-1.20.1.tar.gz"

download:
	curl --connect-timeout 10 -m 20 ${NGINX_DOWNLOAD_URL}/nginx-${NGINX_VERSION}.tar.gz \
		-o ${RESOURCE_DIR}/nginx-${NGINX_VERSION}.tar.gz

replace:
	sed -i "s#NGINX_VERSION#${NGINX_VERSION}#" ${SPECS_DIR}/nginx-el7.spec

build:
	yum install -y rpm-build dos2unix
	rpmbuild -ba nginx-rpm/rpmbuild/SPECS/nginx-el7.spec

all: download replace build