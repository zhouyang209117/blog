#!/bin/bash

cd /data/k8s
python etcd.py $1 $2 $3 $4
cp etcd_config /opt/etcd/cfg/etcd
cp ca*pem server*pem /opt/etcd/ssl
cp etcd /opt/etcd/bin/
cp etcdctl /opt/etcd/bin/
cp etcd.service /usr/lib/systemd/system
mkdir /data/etcd_dir