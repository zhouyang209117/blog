#!/bin/bash
software_dir=/data/k8s_software


# 清环境
rm -f *.pem
if [[ ! -d /usr/local/bin ]]; then
  mkdir /usr/local/bin
fi
if [[ ! -f /usr/local/bin/cfssl ]]; then
    cp $software_dir/cfssl_linux-amd64 /usr/local/bin/cfssl
fi
if [[ ! -f /usr/local/bin/cfssljson ]]; then
    cp $software_dir/cfssljson_linux-amd64 /usr/local/bin/cfssljson
fi
if [[ ! -f /usr/local/bin/cfssl-certinfo ]]; then
    cp $software_dir/cfssl-certinfo_linux-amd64 /usr/bin/cfssl-certinfo
fi
chmod +x /usr/local/bin/cfssl
chmod +x /usr/local/bin/cfssljson
chmod +x /usr/bin/cfssl-certinfo
python create_etcd_server_csr.py
# 生成证书
cfssl gencert -initca ./cert/etcd/ca-csr.json | cfssljson -bare ca -
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=./cert/etcd/ca-config.json \
-profile=www ./cert/etcd/server-csr.json | cfssljson -bare server

if [[ ! -f etcd-v3.2.12-linux-amd64.tar.gz ]]; then
    cp $software_dir/etcd-v3.2.12-linux-amd64.tar.gz .
fi
if [[ ! -d etcd-v3.2.12-linux-amd64 ]]; then
  tar -zxvf etcd-v3.2.12-linux-amd64.tar.gz
fi