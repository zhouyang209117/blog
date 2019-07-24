# coding: utf-8
import sys

host_ip = sys.argv[1]

kubelet_opts = """
KUBELET_OPTS="                                                  \\
--logtostderr=true                                              \\
--v=4                                                           \\
--hostname-override={}                                          \\
--kubeconfig=/opt/kubernetes/cfg/kubelet.kubeconfig             \\
--bootstrap-kubeconfig=/opt/kubernetes/cfg/bootstrap.kubeconfig \\
--config=/opt/kubernetes/cfg/kubelet.config                     \\
--cert-dir=/opt/kubernetes/ssl                                  \\
--pod-infra-container-image=registry.cn-hangzhou.aliyuncs.com/google-containers/pause-amd64:3.0"
"""
with open("kubelet_opts.txt", mode="w") as f:
    f.write(kubelet_opts.format(host_ip))

kubelet_config = """
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
address: {}
port: 10250
readOnlyPort: 10255
cgroupDriver: cgroupfs
clusterDNS: ["10.0.0.2"]
clusterDomain: cluster.local.
failSwapOn: false
authentication:
  anonymous:
    enabled: true
"""
with open("kubelet_config.txt", mode="w") as f:
    f.write(kubelet_config.format(host_ip))

kubelet_service = """
[Unit]
Description=Kubernetes Kubelet
After=docker.service
Requires=docker.service
[Service]
EnvironmentFile=/opt/kubernetes/cfg/kubelet
ExecStart=/opt/kubernetes/bin/kubelet $KUBELET_OPTS
Restart=on-failure
KillMode=process
[Install]
WantedBy=multi-user.target
"""
with open("kubelet_service.txt", mode="w") as f:
    f.write(kubelet_service)

kube_proxy_opts = """
KUBE_PROXY_OPTS="--logtostderr=true              \\
  --v=4                                          \\
  --hostname-override={}                         \\
  --cluster-cidr=10.0.0.0/24                     \\
  --kubeconfig=/opt/kubernetes/cfg/kube-proxy.kubeconfig"
"""
with open("kube_proxy_opts.txt", mode="w") as f:
    f.write(kube_proxy_opts.format(host_ip))

kube_proxy_service = """
[Unit]
Description=Kubernetes Proxy
After=network.target
[Service]
EnvironmentFile=-/opt/kubernetes/cfg/kube-proxy
ExecStart=/opt/kubernetes/bin/kube-proxy $KUBE_PROXY_OPTS
Restart=on-failure
[Install]
WantedBy=multi-user.target
"""
with open("kube_proxy_service.txt", mode="w") as f:
    f.write(kube_proxy_service)

