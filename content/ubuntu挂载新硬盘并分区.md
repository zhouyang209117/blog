# ubuntu挂载新硬盘并分区
* 把硬盘通过usb或者SATA线连好
* 然后执行
```
sudo fdisk -l
```
可以看到所有盘(包括未挂载的),类似如下所示:
```
Disk /dev/sdb: 29.3 GiB, 31457280000 bytes, 61440000 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x56f48570
```
再执行
```
df -hT
```
可以看到所有已经挂载的盘.类似如下所示:
```
tmpfs          tmpfs     1.6G  2.1M  1.6G   1% /run
/dev/nvme0n1p2 ext4      938G  714G  176G  81% /
tmpfs          tmpfs     7.8G   47M  7.7G   1% /dev/shm
tmpfs          tmpfs     5.0M  4.0K  5.0M   1% /run/lock
tmpfs          tmpfs     7.8G     0  7.8G   0% /sys/fs/cgroup
/dev/loop1     squashfs  161M  161M     0 100% /snap/gnome-3-28-1804/116
/dev/loop2     squashfs  384K  384K     0 100% /snap/gnome-characters/550
/dev/loop3     squashfs   63M   63M     0 100% /snap/gtk-common-themes/1506
```
对比fdisk -l和df -hT的结果,确定哪个盘是没有挂载的.以上面的输出为例,/dev/sdb没有被挂载,也没有被分区.
* 如果想对/dev/sdb分一个区,执行
```
sudo fdisk /dev/sdb
n    # n表示新建分区
```
输出
```
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p):
```
输入p,表示是主分区,有如下输出
```
Partition number (1-4, default 1):
```
表示可以分配的分区编号有1-4,直接回车即可(表示选的默认1).有类似如下输出
```
First sector (2048-61439999, default 2048):
Last sector, +sectors or +size{K,M,G,T,P} (2048-61439999, default 61439999):
Created a new partition 1 of type 'Linux' and of size 29.3 GiB.
```
因为要分1个区,所以不用修改First sector,Last sector默认回车即可.最后输入w保存,看到类似如下输出说明分区成功.
```
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```
这时再执行sudo fdisk -l有类似如下输出
```
Disk /dev/sdb: 29.3 GiB, 31457280000 bytes, 61440000 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x56f48570

Device     Boot Start      End  Sectors  Size Id Type
/dev/sdb1        2048 61439999 61437952 29.3G 83 Linux
```
其中/dev/sdb1就是我们刚才分的区,大小是29.3G.执行下面命令格式化分区
```
sudo mkfs.ext4 /dev/sdb1
```
有类似如下输出说明格式化成功.
```
mke2fs 1.44.1 (24-Mar-2018)
Creating filesystem with 7679744 4k blocks and 1921360 inodes
Filesystem UUID: 2c8d1a3c-dee3-4ffe-84d0-17c9640aa40a
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
	4096000

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information:
done
```
再执行如下命令新建目录/data1再把分区/dev/sdb1挂载到目录/data1.
```
sudo mkdir /data1
sudo mount /dev/sdb1 /data1
```
这时再执行df -hT能看到类似如下输出
```
...
/dev/sdb1      ext4       29G   45M   28G   1% /data1
...
```
说明已经挂载成功.
目前/data1仅root用户有写权限.假定一个普通用户是zhou,所在用户组是zhou.执行如下命令给zhou读写权限.
```
sudo chown -R zhou.zhou /data1
```
若要保证重启后挂载还在,编辑/etc/fstab文件,在最后添加如下内容
```
/dev/sdb1 /data1 ext4 defaults 0 0
```
* 如果对想/dev/sdb分多个区,流程基本相同,不同的是填Last sector不能填默认.假定要分2个区,第1个10G,第2个剩下所有.Last sector应填+10G
之后用w保存,然后再输入n新建下一个分区.之后操作步骤都是相同的.
## 参考资料
[buntu下添加硬盘，分区以及自动挂载](https://www.jianshu.com/p/ec5579ef15a6)