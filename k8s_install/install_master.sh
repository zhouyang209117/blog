#!/bin/bash
software_dir=/data/k8s_software

# 清环境
rm -f *.pem
python create_master_server_csr.py
# 生成证书
cfssl gencert -initca ./cert/k8s/ca-csr.json | cfssljson -bare ca -
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=./cert/k8s/ca-config.json \
    -profile=kubernetes ./cert/k8s/server-csr.json | cfssljson -bare server
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=./cert/k8s/ca-config.json \
    -profile=kubernetes ./cert/k8s/admin-csr.json | cfssljson -bare admin
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=./cert/k8s/ca-config.json \
    -profile=kubernetes ./cert/k8s/kube-proxy-csr.json | cfssljson -bare kube-proxy

software_dir=/data/k8s_software
if [[ ! -f kubernetes-server-linux-amd64.tar.gz ]]; then
    cp $software_dir/kubernetes-server-linux-amd64.tar.gz .
fi
if [[ ! -d kubernetes ]]; then
  tar -zxvf kubernetes-server-linux-amd64.tar.gz
fi
