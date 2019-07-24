# coding: utf-8


def get_masterlist():
    with open("hosts_master") as f:
        for index, line in enumerate(f):
            if index == 1:
                arr = line.split(" ")
                arr1 = arr[1].split("=")
                return arr1[1]


with open("./cert/k8s/server-csr.json.tpl") as f1, open("./cert/k8s/server-csr.json", mode="w") as f2:
    content = f1.read()
    host = get_masterlist()
    f2.write(content.replace("MASTER_LIST", "\"" + host + "\","))
