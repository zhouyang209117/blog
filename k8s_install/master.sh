#!/bin/bash

cd /data/k8s
python master.py $1 $2
cp kube-apiserver kube-scheduler kube-controller-manager kubectl /opt/kubernetes/bin
cp api_server_config.txt /opt/kubernetes/cfg/kube-apiserver
cp api_server_service.txt /usr/lib/systemd/system/kube-apiserver.service
cp token.txt /opt/kubernetes/cfg/token.csv
cp kube-scheduler.txt /opt/kubernetes/cfg/kube-scheduler
cp kube_scheduler_service.txt /usr/lib/systemd/system/kube-scheduler.service
cp controller_manager_opts.txt /opt/kubernetes/cfg/kube-controller-manager
cp controller_manager_service.txt /usr/lib/systemd/system/kube-controller-manager.service
cp server.pem server-key.pem ca.pem ca-key.pem /opt/kubernetes/ssl
systemctl daemon-reload
systemctl enable kube-apiserver
systemctl restart kube-apiserver

sleep 3
systemctl daemon-reload
systemctl enable kube-scheduler
systemctl restart kube-scheduler

sleep 3
systemctl daemon-reload
systemctl enable kube-controller-manager
systemctl restart kube-controller-manager