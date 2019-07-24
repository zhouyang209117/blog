# coding: utf-8
import sys


def get_cluster(alias_list, hosts_list):
    assert len(alias_list) == len(hosts_list)
    result = ""
    for x, y in zip(alias_list, hosts_list):
        result += ("{}=https://{}:2380,".format(x, y))
    result = result[: -1]
    return "\"{}\"".format(result)


host_alias = sys.argv[1]
host_ip = sys.argv[2]
hosts_list = sys.argv[3]
alias_list = sys.argv[4]

with open("etcd_config", mode="w") as f:
    # member
    f.write("ETCD_NAME=\"{}\"\n".format(host_alias))
    f.write("ETCD_DATA_DIR=\"/data/etcd_dir\"\n")
    f.write("ETCD_LISTEN_PEER_URLS=\"https://{}:2380\"\n".format(host_ip))
    f.write("ETCD_LISTEN_CLIENT_URLS=\"https://{}:2379\"\n".format(host_ip))
    # cluster
    f.write("ETCD_INITIAL_ADVERTISE_PEER_URLS=\"https://{}:2380\"\n".format(host_ip))
    f.write("ETCD_ADVERTISE_CLIENT_URLS=\"https://{}:2379\"\n".format(host_ip))
    f.write("ETCD_INITIAL_CLUSTER={}\n".format(get_cluster(alias_list.split(","), hosts_list.split(","))))
    f.write("ETCD_INITIAL_CLUSTER_TOKEN=\"etcd-cluster\"\n")
    f.write("ETCD_INITIAL_CLUSTER_STATE=\"new\"\n")

etcd_service = """
Description=Etcd Server
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
EnvironmentFile=/opt/etcd/cfg/etcd
ExecStart=/opt/etcd/bin/etcd                                          \\
--name=${ETCD_NAME}                                                   \\
--data-dir=${ETCD_DATA_DIR}                                           \\
--listen-peer-urls=${ETCD_LISTEN_PEER_URLS}                           \\
--listen-client-urls=${ETCD_LISTEN_CLIENT_URLS},http://127.0.0.1:2379 \\
--advertise-client-urls=${ETCD_ADVERTISE_CLIENT_URLS}                 \\
--initial-advertise-peer-urls=${ETCD_INITIAL_ADVERTISE_PEER_URLS}     \\
--initial-cluster=${ETCD_INITIAL_CLUSTER}                             \\
--initial-cluster-token=${ETCD_INITIAL_CLUSTER_TOKEN}                 \\
--initial-cluster-state=new                                           \\
--cert-file=/opt/etcd/ssl/server.pem                                  \\
--key-file=/opt/etcd/ssl/server-key.pem                               \\
--peer-cert-file=/opt/etcd/ssl/server.pem                             \\
--peer-key-file=/opt/etcd/ssl/server-key.pem                          \\
--trusted-ca-file=/opt/etcd/ssl/ca.pem                                \\
--peer-trusted-ca-file=/opt/etcd/ssl/ca.pem
Restart=on-failure
LimitNOFILE=65536
[Install]
WantedBy=multi-user.target
"""
with open("etcd.service", mode="w") as f:
    f.write(etcd_service)
