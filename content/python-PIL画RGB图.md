# python PIL画RGB图

```
# coding: utf-8

from PIL import Image
import numpy as np

a = np.ones((100, 200, 3), dtype=np.uint8)
a[:, :, 0] = 255
im = Image.fromarray(a, 'RGB')
im.save("aa.jpg", "JPEG")
```
fromarray第一个能数为3维数组时,3维数组的每一维分别表示图片的高,宽,通道数(RGB),上面的代码会画一个高100像素,宽200像素的红色图片.