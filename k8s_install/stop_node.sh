#!/bin/bash

systemctl stop kubelet
systemctl stop kube-proxy

kubectl delete node 192.0.0.3
kubectl delete node 192.0.0.4