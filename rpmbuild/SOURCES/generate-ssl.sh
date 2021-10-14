#!/usr/bin/env bash
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
openssl x509 -req -sha512 -days 365 \
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