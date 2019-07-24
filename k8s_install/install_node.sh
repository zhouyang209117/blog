#!/bin/bash
# 将kubelet-bootstrap用户绑定到系统集群角色
kubectl create clusterrolebinding kubelet-bootstrap \
    --clusterrole=system:node-bootstrapper          \
    --user=kubelet-bootstrap
# 创建kubelet bootstrapping kubeconfig
BOOTSTRAP_TOKEN=674c457d4dcf2eefe4920d7dbb6b0ddc
KUBE_APISERVER="https://192.0.0.2:6443"
# 设置集群参数
kubectl config set-cluster kubernetes              \
    --certificate-authority=./ca.pem               \
    --embed-certs=true                             \
    --server=${KUBE_APISERVER}                     \
    --kubeconfig=bootstrap.kubeconfig
# 设置客户端认证参数
kubectl config set-credentials kubelet-bootstrap   \
    --token=${BOOTSTRAP_TOKEN}                     \
    --kubeconfig=bootstrap.kubeconfig
# 设置上下文件参数
kubectl config set-context default                 \
    --cluster=kubernetes                           \
    --user=kubelet-bootstrap                       \
    --kubeconfig=bootstrap.kubeconfig
# 设置默认上下文
kubectl config use-context default                 \
    --kubeconfig=bootstrap.kubeconfig
# 创建kube-proxy kubeconfig文件
kubectl config set-cluster kubernetes              \
    --certificate-authority=./ca.pem               \
    --embed-certs=true                             \
    --server=${KUBE_APISERVER}                     \
    --kubeconfig=kube-proxy.kubeconfig
kubectl config set-credentials kube-proxy          \
    --client-certificate=./kube-proxy.pem          \
    --client-key=./kube-proxy-key.pem              \
    --embed-certs=true                             \
    --kubeconfig=kube-proxy.kubeconfig
kubectl config set-context default                 \
    --cluster=kubernetes                           \
    --user=kube-proxy                              \
    --kubeconfig=kube-proxy.kubeconfig
kubectl config use-context default                 \
    --kubeconfig=kube-proxy.kubeconfig