#!/bin/bash

cd /data/k8s
python node.py $1
mv kubelet kube-proxy /opt/kubernetes/bin
mv bootstrap.kubeconfig /opt/kubernetes/cfg/bootstrap.kubeconfig
mv kube-proxy.kubeconfig /opt/kubernetes/cfg/kube-proxy.kubeconfig
mv kubelet_opts.txt /opt/kubernetes/cfg/kubelet
mv kubelet_config.txt /opt/kubernetes/cfg/kubelet.config
mv kubelet_service.txt /usr/lib/systemd/system/kubelet.service
mv kube_proxy_opts.txt /opt/kubernetes/cfg/kube-proxy
mv kube_proxy_service.txt /usr/lib/systemd/system/kube-proxy.service
rm -f /opt/kubernetes/ssl/*
systemctl daemon-reload
systemctl enable kubelet
systemctl restart kubelet

systemctl daemon-reload
systemctl enable kube-proxy
systemctl restart kube-proxy