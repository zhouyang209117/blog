## 导数偏导数的数学定义
参考资料1和2中对导数偏导数的定义都非常明确.导数和偏导数都是函数对自变量而言.从数学定义上讲,求导或者求偏导只有函数对自变量,其余任何情况都是错的.但是很多机器学习的资料和开源库都涉及到标量对向量求导.比如下面这个pytorch的例子.

```
import torch
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = x ** 2 + 2
z = torch.sum(y)
z.backward()
print(x.grad)
```
简单解释下,设$x=[x_1,x_2,x_3]$,则
$$
\begin{equation*}
   z=x_1^2+x_2^2+x_3^2+6
\end{equation*}
$$
则
$$
\begin{equation*}
    \frac{\partial z}{\partial x_1}=2x_1
\end{equation*}
$$
$$
\begin{equation*}
    \frac{\partial z}{\partial x_2}=2x_2
\end{equation*}
$$
$$
\begin{equation*}
    \frac{\partial z}{\partial x_3}=2x_3
\end{equation*}
$$
将$x_1=1.0$,$x_2=2.0$,$x_3=3.0$代入就可以得到
$$
\begin{equation*}
    (\frac{\partial z}{\partial x_1},\frac{\partial z}{\partial x_2},\frac{\partial z}{\partial x_3})=(2x_1,2x_2,2x_3)=(2.0,4.0,6.0)
\end{equation*}
$$
结果是和pytorch的输出是一样的.反过来想想,其实所谓的"标量对向量求导"本质上是函数对各个自变量求导,这里只是把各个自变量看成一个向量.和数学上的定义并不矛盾.

## backward的gradient参数作用
现在有如下问题,已知
$$
\begin{equation*}
   y_1=x_1x_2x_3
\end{equation*}
$$
$$
\begin{equation*}
   y_2=x_1+x_2+x_3
\end{equation*}
$$
$$
\begin{equation*}
   y_3=x_1+x_2x_3
\end{equation*}
$$
$$
\begin{equation*}
   A=f(y_1,y_2,y_3)
\end{equation*}
$$
其中函数$f(y_1,y_2,y_3)$的具体定义未知,现在求
$$
\begin{equation*}
   \frac{\partial A}{\partial x_1}=?
\end{equation*}
$$
$$
\begin{equation*}
   \frac{\partial A}{\partial x_2}=?
\end{equation*}
$$
$$
\begin{equation*}
   \frac{\partial A}{\partial x_3}=?
\end{equation*}
$$
根据参考资料2中讲的多元复合函数的求导法则.
$$
\begin{equation*}
   \frac{\partial A}{\partial x_1}=\frac{\partial A}{\partial y_1}\frac{\partial y_1}{\partial x_1}+\frac{\partial A}{\partial y_2}\frac{\partial y_2}{\partial x_1}+\frac{\partial A}{\partial y_3}\frac{\partial y_3}{\partial x_1}
\end{equation*}
$$
$$
\begin{equation*}
   \frac{\partial A}{\partial x_2}=\frac{\partial A}{\partial y_1}\frac{\partial y_1}{\partial x_2}+\frac{\partial A}{\partial y_2}\frac{\partial y_2}{\partial x_2}+\frac{\partial A}{\partial y_3}\frac{\partial y_3}{\partial x_2}
\end{equation*}
$$
$$
\begin{equation*}
   \frac{\partial A}{\partial x_3}=\frac{\partial A}{\partial y_1}\frac{\partial y_1}{\partial x_3}+\frac{\partial A}{\partial y_2}\frac{\partial y_2}{\partial x_3}+\frac{\partial A}{\partial y_3}\frac{\partial y_3}{\partial x_3}
\end{equation*}
$$
上面3个等式可以写成矩阵相乘的形式.如下
$$
\begin{equation}\label{simple}
    [\frac{\partial A}{\partial x_1},\frac{\partial A}{\partial x_2},\frac{\partial A}{\partial x_3}]=
    [\frac{\partial A}{\partial y_1},\frac{\partial A}{\partial y_2},\frac{\partial A}{\partial y_3}]
   \left[
   \begin{matrix}
   \frac{\partial y_1}{\partial x_1} & \frac{\partial y_1}{\partial x_2} & \frac{\partial A}{\partial x_3}  \\
   \frac{\partial y_2}{\partial x_1} & \frac{\partial y_2}{\partial x_2} & \frac{\partial A}{\partial x_3}  \\
   \frac{\partial y_3}{\partial x_1} & \frac{\partial y_3}{\partial x_2} & \frac{\partial A}{\partial x_3}
   \end{matrix}
   \right]
\end{equation}
$$
其中
$$
\begin{equation*}
   \left[
   \begin{matrix}
   \frac{\partial y_1}{\partial x_1} & \frac{\partial y_1}{\partial x_2} & \frac{\partial y_1}{\partial x_3}  \\
   \frac{\partial y_2}{\partial x_1} & \frac{\partial y_2}{\partial x_2} & \frac{\partial y_2}{\partial x_3}  \\
   \frac{\partial y_3}{\partial x_1} & \frac{\partial y_3}{\partial x_2} & \frac{\partial y_3}{\partial x_3}
   \end{matrix}
   \right]
\end{equation*}
$$
叫作雅可比(Jacobian)式.雅可比式可以根据已知条件求出.现在只要知道$[\frac{\partial A}{\partial y_1},\frac{\partial A}{\partial y_2},\frac{\partial A}{\partial y_3}]$的值,哪怕不知道$f(y_1,y_2,y_3)$的具体形式也能求出来$[\frac{\partial A}{\partial x_1},\frac{\partial A}{\partial x_2},\frac{\partial A}{\partial x_3}]$. 那现在的现在的问题是:
怎么样才能求出
$$
\begin{equation*}
    [\frac{\partial A}{\partial y_1},\frac{\partial A}{\partial y_2},\frac{\partial A}{\partial y_3}]
\end{equation*}
$$
答案是由pytorch的backward函数的gradient参数提供.**这就是gradient参数的作用**. 参数gradient能解决什么问题,有什么实际的作用呢?说实话,因为我才接触到pytorch,还真没有见过现实中怎么用gradient参数.但是目前可以通过数学意义来理解,就是可以忽略复合函数某个位置之前的所有函数 的具体形式,直接给定一个梯度来求得对各个自变量的偏导.
上面各个方程用代码表示如下所示:
```
# coding utf-8
import torch

x1 = torch.tensor(1, requires_grad=True, dtype=torch.float)
x2 = torch.tensor(2, requires_grad=True, dtype=torch.float)
x3 = torch.tensor(3, requires_grad=True, dtype=torch.float)
y = torch.randn(3)
y[0] = x1 * x2 * x3
y[1] = x1 + x2 + x3
y[2] = x1 + x2 * x3
x = torch.tensor([x1, x2, x3])
y.backward(torch.tensor([0.1, 0.2, 0.3], dtype=torch.float))
print(x1.grad)
print(x2.grad)
print(x3.grad)
```
按照上用的推导方法
$$
\begin{equation*}
\begin{split}
    [\frac{\partial A}{\partial x_1},\frac{\partial A}{\partial x_2},\frac{\partial A}{\partial x_3}]
    &=[\frac{\partial A}{\partial y_1},\frac{\partial A}{\partial y_2},\frac{\partial A}{\partial y_3}]
   \left[
   \begin{matrix}
   x_2x_3 & x_1x_3 & x_1x_2 \\
   1      & 1      & 1      \\
   1      & x_3    & x_2
   \end{matrix}
   \right]
   &=[0.1,0.2,0.3]
   \left[
   \begin{matrix}
   6 & 3 & 2 \\
   1 & 1 & 1 \\
   1 & 3 & 2
   \end{matrix}
   \right]
   &=[1.1,1.4,1.0]
\end{split}
\end{equation*}
$$
和代码的运行结果是一样的.
## 参考资料
1. 同济大学数学系,高等数学第七版上册,高等教育出版社,p75-76, 2015.
1. 同济大学数学系,高等数学第七版下册,高等教育出版社,p78-80,p88-91, 2015.
1. Calculus,Thirteenth Edition,p822, 2013.
1. [详解Pytorch 自动微分里的（vector-Jacobian product）](https://zhuanlan.zhihu.com/p/65609544)
1. [PyTorch 的 backward 为什么有一个 grad_variables 参数？）](https://zhuanlan.zhihu.com/p/29923090)