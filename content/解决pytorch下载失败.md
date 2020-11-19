# 解决pytorch下载失败
因为国内网络问题,即便anaconda配制了清华源,有时候安装pytorch gpu版本的时候还会失败.从安装pytorch1.7.0 gpu版本的实际情况看,有时按
pytorch官方文档的命令装一两天都有装不上.这里总结了一个步骤，虽然也比较慢，但最终还是可以装好.也算是一个在较差网络环境下的"最佳实践".
1. 在xx云上买一个国外的云主机.
1. 在云主机上装miniconda. 大家可能更熟悉anaconda,miniconda和anaconda相比只保留了python环境创建,下载第三方包功能,
去掉了jupter notebook的功能.
1. 用国外云主机的miniconda安装gpu版本的pytorch,命令如下:
```
conda create -n pytorch1.7.0 python=3.8.5
conda activate pytorch1.7.0
conda install pytorch torchvision torchaudio cudatoolkit=11.0 -c pytorch
```
我买的云主机在德国,十几分钟就安装好了,再也不用配制conda的源了.
1. pytorch被安装到了$CONDA_HOME/envs/pytorch1.7.0目录下. 把pytorch1.7.0目录打包成压缩包,压缩包有2G多.
1. 用scp命令把压缩包拖到本地,这个过程比较漫长,我大概弄了两三个小时. 成功后解压到本地的$CONDA_HOME/envs/pytorch1.7.0目录.
1. 修改$CONDA_HOME/envs/pytorch1.7.0/bin/pip文件,把第1行python的位置修改成和本地机一致(之前是云主机的).之后就可以按
以前的方法使用pytorch1.7.0环境了.
1. 比较绕的方法,没有办法的办法.没有办法情况下的“最佳实践”
## 参考资料
[pytorch官方文档](https://pytorch.org/)
[conda国内源官网](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
[miniconda官网](https://docs.conda.io/en/latest/miniconda.html)