#!/bin/bash
software_dir=/data/k8s_software
if [[ ! -f kubernetes-server-linux-amd64.tar.gz ]]; then
    cp $software_dir/kubernetes-server-linux-amd64.tar.gz .
fi
if [[ ! -d kubernetes ]]; then
    tar -zxvf kubernetes-server-linux-amd64.tar.gz
fi
cd kubernetes
if [[ ! -d kubernetes-src ]]; then
    mkdir kubernetes-src
    tar -zxvf kubernetes-src.tar.gz -C kubernetes-src
fi