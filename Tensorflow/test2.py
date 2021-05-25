import numpy as np
import tensorflow as tf

A = tf.reshape(tf.range(9), (3, 3))
B = tf.constant([[1, 2, 3], [2, 0, 4], [3, 4, 5]])

def is_symmetric(m):
    if (tf.transpose(m) == m).numpy().all():  # any()是任一个为True就为True
        print("是对称矩阵")


is_symmetric(A)
is_symmetric(B)

a = np.ones((3, 3))
print(a.all())
a = np.zeros((3, 3))
print(a.all(), a.any())
a[0, 0] = 1
print(a.all(), a.any())
