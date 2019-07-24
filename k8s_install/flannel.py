#!/bin/bash
import sys
flannel_opts = """
FLANNEL_OPTIONS="--etcd-endpoints={}        \\
-etcd-cafile=/opt/etcd/ssl/ca.pem           \\
-etcd-certfile=/opt/etcd/ssl/server.pem     \\
-etcd-keyfile=/opt/etcd/ssl/server-key.pem"
"""

flannel_service = """
[Unit]
Description=Flanneld overlay address etcd agent
After=network-online.target network.target
Before=docker.service
[Service]
Type=notify
EnvironmentFile=/opt/kubernetes/cfg/flanneld
ExecStart=/opt/kubernetes/bin/flanneld --ip-masq $FLANNEL_OPTIONS
ExecStartPost=/opt/kubernetes/bin/mk-docker-opts.sh -k DOCKER_NETWORK_OPTIONS -d /run/flannel/subnet.env
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
with open("flanneld_config", mode="w") as f:
    hosts = get_hosts(hosts_list)
    f.write(flannel_opts.format(hosts))

with open("flanneld.service", mode="w") as f:
    f.write(flannel_service)
