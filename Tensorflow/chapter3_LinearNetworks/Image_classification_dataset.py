import time

import numpy as np
import tensorflow as tf
from d2l import tensorflow as d2l
import matplotlib.pyplot as plt
import cv2

d2l.use_svg_display()

# (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.fashion_mnist.load_data()

# # 可视化纵向排列
# b = train_images[:10]
# print(train_labels[:10])
# im_list = b.reshape((28 * 10, 28))
# cv2.imshow('im_list_vertical', im_list)
# cv2.waitKey(0)
#
# # 可视化横向排列
# b = train_images[:10]
# print(train_labels[:10])
# im_list = np.hstack(b)
# cv2.imshow('im_list_horizontal', im_list)
# cv2.waitKey(0)

# # 可视化矩阵
# n = 10
# rows = []
# for i in range(n):
#     rows.append(np.hstack(train_images[i * n:i * n + n]))
# im_matrix = np.vstack(rows)
# cv2.imshow('im_matrix', im_matrix)
# cv2.waitKey(0)


def get_fashion_mnist_labels(labels):  #@save
    """返回Fashion-MNIST数据集的文本标签。"""
    text_labels = [
        't-shirt', 'trouser', 'pullover', 'dress', 'coat', 'sandal', 'shirt',
        'sneaker', 'bag', 'ankle boot']
    return [text_labels[int(i)] for i in labels]


def show_images(imgs, num_rows, num_cols, titles=None, scale=1.5):  #@save
    """绘制图像列表。"""
    figsize = (num_cols * scale, num_rows * scale)
    _, axes = d2l.plt.subplots(num_rows, num_cols, figsize=figsize)
    axes = axes.flatten()
    for i, (ax, img) in enumerate(zip(axes, imgs)):
        ax.imshow(img.numpy())
        # ax.imshow(img.numpy(), 'gray')  # 原始的灰度图
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        if titles:
            ax.set_title(titles[i])
    return axes


# # 显示单个图像，可以设置各种模式（灰度，binary等，默认是三通道模式）
# plt.figure()
# # plt.imshow(train_images[0], cmap=plt.cm.binary)
# # plt.imshow(train_images[0], cmap='gray')
# plt.imshow(train_images[0])
# plt.colorbar()
# # plt.grid(False)
# plt.show()

# 显示多个图像
# X = tf.constant(train_images[:18])
# y = tf.constant(train_labels[:18])
# show_images(X, 2, 9, titles=get_fashion_mnist_labels(y))
# d2l.plt.show()

# 读取小批量
batch_size = 256
# 首先，这里要传元组。其次，居然先batch再shuffle？？？
# 原代码这里的shuffle仅对batches进行shuffle，意义不大
# 原代码先batch再shuffle，错误，应该先shuffle再batch
# train_iter = tf.data.Dataset.from_tensor_slices((train_images, train_labels)).batch(
#     batch_size).shuffle(len(train_images))
train_iter = tf.data.Dataset.from_tensor_slices((train_images, train_labels)).shuffle(
    len(train_images)).batch(batch_size)

timer = d2l.Timer()
for X, y in train_iter:
    continue
print(f'{timer.stop():.2f} sec')


def load_data_fashion_mnist(batch_size, resize=None):  #@save
    """下载Fashion-MNIST数据集，然后将其加载到内存中。"""
    mnist_train, mnist_test = tf.keras.datasets.fashion_mnist.load_data()
    # 将所有数字除以255，使所有像素值介于0和1之间，在最后添加一个批处理维度，
    # 并将标签转换为int32。
    process = lambda X, y: (tf.expand_dims(X, axis=3) / 255,  # 这里扩展维度有什么用？后续待考察
                            tf.cast(y, dtype='int32'))
    resize_fn = lambda X, y: (tf.image.resize_with_pad(X, resize, resize)
                              if resize else X, y)
    return (tf.data.Dataset.from_tensor_slices(
            process(*mnist_train)).shuffle(len(mnist_train[0])).batch(batch_size).map(resize_fn),
        tf.data.Dataset.from_tensor_slices(process(*mnist_test)).batch(batch_size).map(resize_fn)
        )


train_iter, test_iter = load_data_fashion_mnist(32, resize=64)
for X, y in train_iter:
    print(X.shape, X.dtype, y.shape, y.dtype)
    print(X[0])
    break
