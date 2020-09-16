# python还原mnist为图片
用numpy的reshape函数可以大大简化代码.

## numpy.reshape
先看一个例子.
```
import numpy as np
arr1 = np.arange(12).reshape(2, 2, 3)
arr2 = np.arange(12).reshape(2, 3, 2)
print(arr1)
print(arr2)
```
初始化一个3维的数组.reshape的作用是用整数0到11填充2*2*3的数组.reshape从最后一维开始填充,然后再填充倒数第二维,一直到第0维.
可以比较arr1,arr2的不同,理解差别.

## 保存图片
mnist格式解析见参考资料2. fromarray第一个参数如果是2维数组,那么第0维是图片的高,第1维是图片的宽.fromarray的model参数,见参考资料3.
L表示8字节的整型.
```
# coding: utf-8
import numpy as np
import struct
from PIL import Image

file_path = "/Users/zhouyang3/ds/train-images-idx3-ubyte"

with open(file_path, 'rb') as f:
    buf = f.read()
    index = 0
    magic, numImages, numRows, numColumns = struct.unpack_from('>IIII', buf, index)  # 读取前4个字节的内容
    size = numImages * numRows * numColumns
    index += struct.calcsize('>IIII')
    im = struct.unpack_from('>{}B'.format(size), buf, index)
    data = np.array(im).astype(np.uint8).reshape(numImages, numRows, numColumns)
    for i in range(10):
        im = Image.fromarray(data[i], 'L')
        im.save("./mnist/{}.png".format(i))
```
## 参考资料
1. [mnist官方文档](!http://yann.lecun.com/exdb/mnist/)
1. [python读取,显示，保存mnist图片](!https://www.cnblogs.com/zhouyang209117/p/6436751.html)
1. [pillow Modes](!https://pillow.readthedocs.io/en/4.2.x/handbook/concepts.html#concept-modes)