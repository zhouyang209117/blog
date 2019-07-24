#!/bin/bash

cd /data/k8s
img_prefix="image: k8s.gcr.io/kubernetes-dashboard"
img_ali="image: registry.cn-hangzhou.aliyuncs.com/kuberneters/kubernetes-dashboard-amd64:v1.10.1"
sed -i 's#'"$img_prefix"'.*#'"$img_ali"'#g' dashboard-controller.yaml
content=`cat dashboard-service.yaml`
node_port="  type: NodePort"
if [[ ! $content =~ $node_port ]]; then
    sed -i '/spec:/a\'"$node_port"'' dashboard-service.yaml
fi
PATH=$PATH:/opt/kubernetes/bin
kubectl apply -f dashboard-configmap.yaml
kubectl apply -f dashboard-rbac.yaml
kubectl apply -f dashboard-secret.yaml
kubectl apply -f dashboard-controller.yaml
kubectl apply -f dashboard-service.yaml
kubectl apply -f k8s-admin.yaml