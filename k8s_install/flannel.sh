#!/bin/bash

cd /data/k8s
python flannel.py $1
mv mk-docker-opts.sh flanneld /opt/kubernetes/bin
cp flanneld_config /opt/kubernetes/cfg/flanneld
cp flanneld.service /usr/lib/systemd/system
docker_config=/usr/lib/systemd/system/docker.service
content=`cat $docker_config`
env="EnvironmentFile="
opts="DOCKER_NETWORK_OPTIONS"
if [[ ! $content =~ $env ]]; then
    sed -i '/Type=notify/a\EnvironmentFile=/run/flannel/subnet.env' $docker_config
fi
if [[ ! $content =~ $opts ]]; then
    sed -i 's#^ExecStart=.*#& $DOCKER_NETWORK_OPTIONS#g' $docker_config
fi
systemctl daemon-reload
systemctl start flanneld
systemctl enable flanneld
systemctl restart docker