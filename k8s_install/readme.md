# kubernetes安装
## 写在前面的话
先介绍单master多node的安装方法.之后再介绍多master的安装方法. kubernetes集群最简单的安装方法是用kubeadm,基本上可以实现"一键安装".对于初学者不建议使用这种方法.kubernetes涉及多个独立的应用,包括etcd,docker,flanneld,apiserver,scheduler,controller-manager,kubelet,kbue-proxy.下面会逐个介绍安装方法和作用,为了描述问题方便.假定有192.0.0.2,192.0.0.3,192.0.0.4三台主机,要确保各个主机ssh互通.主机的角色如下所示:

| 角色 | IP | 组件 |
| :------:| :---: |:---: |
| k8s-master, k8s-node1 | 192.0.0.2 | etcd, kube-apiserver, kube-controller-manager, kube-scheduler, docker, ansible, flannel, kubelet, kube-proxy |
| k8s-node2 | 192.0.0.3 | etcd, kubelet, kube-proxy, docker, flannel |
| k8s-node3 | 192.0.0.4 | etcd, kubelet, kube-proxy, docker, flannel |

所使用系统和组件版本

| 软件 | 版本 |
| :------:| :---: |
| OS | CentOS Linux release 7.5.1804 (Core) |
| Docker | 18.09.3 |
| Kubernetes | 1.12 |
| ansible | 随意 |

主机192.0.0.2上用ansible,通过主机192.0.0.2向其它机器上装各种组件.首先要下载各个组件.在192.0.0.2的/data/k8s_software文件夹下执行
```
# 认证
wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
# etcd
wget https://github.com/etcd-io/etcd/releases/download/v3.2.12/etcd-v3.2.12-linux-amd64.tar.gz
# flannel
wget https://github.com/coreos/flannel/releases/download/v0.10.0/flannel-v0.10.0-linux-amd64.tar.gz
wget https://storage.googleapis.com/kubernetes-release/release/v1.12.1/kubernetes-server-linux-amd64.tar.gz
```

## 安装etcd
* 根据实际情况修改hosts_etcd配制文件,20021是ssh端口,通常是22.这里写成20021是因为公司限制了22端口.
* 执行
```
sh install_etcd.sh
```
生成了ssl的key,解压etcd-v3.2.12-linux-amd64.tar.gz

* 执行
```
anbile-playbook -i hosts_etcd ansible_etcd.yml
```
这个ansible脚本是把etcd组件和ssl key传到各个机器上,生成配制.不再描述细节,可以看代码.

* 在每个etcd机器上执行
```
systemctl start etcd
systemctl enable etcd
```

* 执行下面命令检查etcd状态
```
/opt/etcd/bin/etcdctl \
--ca-file=/opt/etcd/ssl/ca.pem --cert-file=/opt/etcd/ssl/server.pem --key-file=/opt/etcd/ssl/server-key.pem \
--endpoints="https://192.0.0.2:2379,https://192.0.0.3:2379,https://192.0.0.4:2379" \
cluster-health
```
如果得到类似下面的输出,说明是正确的.
```
member 4663da11799a0347 is healthy: got healthy result from https://192.0.0.2:2379
member abb5a8a4a7c8e1cd is healthy: got healthy result from https://192.0.0.4:2379
member ca4e95401fe5dd82 is healthy: got healthy result from https://192.0.0.3:2379
cluster is healthy
```
如果输出有异常,通过tailf /var/log/message或journalctl -u etcd看日志.

## 安装docker
* 执行
```
anbile-playbook -i hosts_etcd ansible_docker.yml
```
* 执行
```
docker -v
```
看能否输出docker的版本.

## 安装flannel
flannel虚拟出一个子网,确保容器之间能通信.
执行
```
sh install_flannel.sh
```
解压.再执行
```
ansible-playbook -i hosts_etcd ansible_flannel.yml
```
把flannel组件上传到各个机器,生成配制文件,启动.执行
```
ps -ef | grep docker
```
看docker是否有--bip选项.有则正常.再执行
```
ip addr
```
查看docker0和flannel.1是不是在一个网段上.
在不同结点上通过docker启动busybox,看相互之间能不能ping通.如果有异常通过
```
journalctl -u flannel
```
查看日志.

## 部署matster节点
* 根据实际情况修改hosts_master里面的ip,注意这里只讨论单master的部署方式.
* 执行
```
sh install_master.sh
```
生成认证,解压压缩包.
* 执行
```
ansible-playbook -i hosts_master ansible_master.yml
```
把组件和认证传到master主机.启动kube-apiserver, kube-scheduler, kube-controller-manager
* 执行
```
kubectl get cs
```
查看scheduler,controller-manager的状态是否是ok.

## 安装node
* 根据实际情况修改hosts_node的ip和端口.
* 执行
```
sh install_node.sh
```
生成配制.
* 执行
```
ansible-playbook -i hosts_node ansible_node.yml
```
把可执行文件和配制传到各个结点.启动服务.
* 执行
```
kubectl get csr
```
正常情况下可以看到结点都是pending状态.
* 执行
```
kubectl certificate approve node-csr-XXXXXXXXXXXXX
```
对所有的node结点执行上面的命令.
* 最后再执行
```
kubectl get node
```
可以看到所有结点都是ready状态.

## 参考资料
* k8s官方文档
* [Kubernetes/K8S入门进阶实战](https://study.163.com/course/courseMain.htm?courseId=1005024008&share=1&shareId=1139090540)