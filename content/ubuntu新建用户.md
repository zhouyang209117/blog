# ubuntu新建用户
先新建一个文件夹,如/data1/user2当作新用户user2的主目录
```
sudo useradd -d /data1/user2 -s /bin/bash user2
```
再把主目录的权限给user2
```
sudo chown user2.user2 /data1/user2
```
设置user2的密码
```
sudo passwd user2
```
新建的用户主目录没有.bashrc,建一个.bashrc再配环境变量也没用.因为ubuntu20.04普通用户登录的时候默认不执行source ~/.bashrc
经测试登录默认执行的是 source \~/.bash_profile,所以要在\~/.bash_profile配制环境变量.比较激进的做法,直接把当前用户的.bashrc
文件拷贝为新用户的.bash_profile
```
sudo cp .bashrc /data1/user2/.bash_profile
sudo chown user2.user2 /data1/user2/.bash_profile
```
如果想删除新用户及所有文件,执行
```
sudo userdel -r user2
```