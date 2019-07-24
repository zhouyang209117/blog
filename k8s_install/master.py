#!/bin/bash
import sys
opts = """
KUBE_APISERVER_OPTS="                                     \\
--logtostderr=true                                        \\
--v=4                                                     \\
--etcd-servers={}                                         \\
--bind-address={}                                         \\
--secure-port=6443                                        \\
--advertise-address={}                                    \\
--allow-privileged=true                                   \\
--service-cluster-ip-range=10.0.0.0/24                    \\
--enable-admission-plugins=NamespaceLifecycle,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota,NodeRestriction \\
--authorization-mode=RBAC,Node                            \\
--kubelet-https=true                                      \\
--enable-bootstrap-token-auth                             \\
--token-auth-file=/opt/kubernetes/cfg/token.csv           \\
--service-node-port-range=30000-50000                     \\
--tls-cert-file=/opt/kubernetes/ssl/server.pem            \\
--tls-private-key-file=/opt/kubernetes/ssl/server-key.pem \\
--client-ca-file=/opt/kubernetes/ssl/ca.pem               \\
--service-account-key-file=/opt/kubernetes/ssl/ca-key.pem \\
--etcd-cafile=/opt/etcd/ssl/ca.pem                        \\
--etcd-certfile=/opt/etcd/ssl/server.pem                  \\
--etcd-keyfile=/opt/etcd/ssl/server-key.pem"
"""

service = """
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/kubernetes/kubernetes
[Service]
EnvironmentFile=-/opt/kubernetes/cfg/kube-apiserver
ExecStart=/opt/kubernetes/bin/kube-apiserver $KUBE_APISERVER_OPTS
Restart=on-failure
[Install]
WantedBy=multi-user.target
"""

def get_hosts(hosts_str):
    hosts = hosts_str.split(",")
    result = ""
    for h in hosts:
        result += "https://{}:2379,".format(h)
    result = result[: -1]
    return result


hosts_list = sys.argv[1]
host = sys.argv[2]
with open("api_server_config.txt", mode="w") as f:
    hosts = get_hosts(hosts_list)
    f.write(opts.format(hosts, host, host))

with open("api_server_service.txt", mode="w") as f:
    f.write(service)

token = "674c457d4dcf2eefe4920d7dbb6b0ddc,kubelet-bootstrap,10001,\"system:kubelet-bootstrap\""
with open("token.txt", mode="w") as f:
    f.write(token)

kube_scheduler_opts = """
KUBE_SCHEDULER_OPTS="--logtostderr=true \\
--v=4                                   \\
--master=127.0.0.1:8080                 \\
--leader-elect"
"""
with open("kube-scheduler.txt", mode="w") as f:
    f.write(kube_scheduler_opts)

kube_scheduler_service = """
[Unit]
Description=Kubernetes Scheduler
Documentation=https://github.com/kubernetes/kubernetes
[Service]
EnvironmentFile=-/opt/kubernetes/cfg/kube-scheduler
ExecStart=/opt/kubernetes/bin/kube-scheduler $KUBE_SCHEDULER_OPTS
Restart=on-failure
[Install]
WantedBy=multi-user.target
"""
with open("kube_scheduler_service.txt", mode="w") as f:
    f.write(kube_scheduler_service)

controller_manager_opts = """
KUBE_CONTROLLER_MANAGER_OPTS="--logtostderr=true                   \\
--v=4                                                              \\
--master=127.0.0.1:8080                                            \\
--leader-elect=true                                                \\
--address=127.0.0.1                                                \\
--service-cluster-ip-range=10.0.0.0/24                             \\
--cluster-name=kubernetes                                          \\
--cluster-signing-cert-file=/opt/kubernetes/ssl/ca.pem             \\
--cluster-signing-key-file=/opt/kubernetes/ssl/ca-key.pem          \\
--root-ca-file=/opt/kubernetes/ssl/ca.pem                          \\
--service-account-private-key-file=/opt/kubernetes/ssl/ca-key.pem  \\
--experimental-cluster-signing-duration=87600h0m0s"
"""
with open("controller_manager_opts.txt", mode="w") as f:
    f.write(controller_manager_opts)

controller_manager_service = """
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/kubernetes/kubernetes
[Service]
EnvironmentFile=-/opt/kubernetes/cfg/kube-controller-manager
ExecStart=/opt/kubernetes/bin/kube-controller-manager $KUBE_CONTROLLER_MANAGER_OPTS
Restart=on-failure
[Install]
WantedBy=multi-user.target
"""
with open("controller_manager_service.txt", mode="w") as f:
    f.write(controller_manager_service)