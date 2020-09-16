# python还原cifar10为图片

```
# coding: utf-8
import pickle as cPickle
from PIL import Image


def unpickle(file):
    with open(file, 'rb') as fo:
        dict = cPickle.load(fo, encoding='iso-8859-1')
    return dict


if __name__ == '__main__':
    filePath = "/Users/zhouyang3/ds/cifar-10-batches-py/data_batch_1"
    data = unpickle(filePath)
    batch_label = data["batch_label"]
    print(batch_label)
    labels = data["labels"]
    print(len(labels))
    dataPic = data["data"]
    print(dataPic.shape)
    filenames = data["filenames"]
    print(len(filenames))
    for i in range(10000):
        a = dataPic[i].reshape(3, 32, 32).transpose(1, 2, 0)
        im = Image.fromarray(a, 'RGB')
        im.save("./pic/{}".format(filenames[i]))
```