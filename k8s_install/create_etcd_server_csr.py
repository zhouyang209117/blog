# coding: utf-8

def get_hostlist():
    with open("hosts_etcd") as f:
        for index, line in enumerate(f):
            if index == 1:
                arr = line.split(" ")
                arr1 = arr[3].split("=")
                return arr1[1].split(",")


with open("./cert/etcd/server-csr.json.tpl") as f1, open("./cert/etcd/server-csr.json", mode="w") as f2:
    content = f1.read()
    hosts = get_hostlist()
    hosts_str = ""
    for host in hosts:
        hosts_str += ("\"" + host + "\",\n")
    hosts_str = hosts_str[: -2]
    f2.write(content.replace("HOST_LIST", hosts_str))
