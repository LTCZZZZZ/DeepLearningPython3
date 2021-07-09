# 可视化数字

import gzip
import pickle
import cv2
import imutils
import numpy as np

f = gzip.open('mnist.pkl.gz', 'rb')
training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
f.close()

# with open('mnist.pkl', 'rb') as f:
#     training_data, validation_data, test_data = pickle.load(f, encoding="latin1")


# print(training_data[0].shape)
a = training_data[0][0]
print(a.shape)

# 下面两行效果完全相同，说明小数的array可以直接显示，另外注意，astype()的参数必须为'uint8'，否则会有问题
# im = (a.reshape((28, 28)) * 255).astype('uint8')
im = (a.reshape((28, 28)))

# im = imutils.resize(im, width=100)

print(im)
cv2.imshow('im', im)
cv2.waitKey(0)
a = a.reshape((784, 1))
print(a.shape)

# 纵向排列
b = training_data[0][:10]
print(training_data[1][:10])
im_list = b.reshape((28 * 10, 28))
cv2.imshow('im_list', im_list)
cv2.waitKey(0)

# 横向排列
d_list = []
for i in range(10):
    d_list.append(im_list[28 * i:28 * i + 28])
im_list2 = np.hstack(d_list)
cv2.imshow('im_list2', im_list2)
cv2.waitKey(0)
