import tensorflow as tf
import numpy as np

a = tf.constant(range(1, 4))
b = tf.constant(range(1, 4))
print(tf.tensordot(a, b, axes=1))  # 14, shape=()

a = tf.constant(range(1, 4), shape=(1, 3))
b = tf.constant(range(1, 4), shape=(3))
# 经测试，此法一般只能作用于矩阵乘向量，会将向量往后增加一个value=1的维度，
# 且最后结果比用 @ 少一个维度(因为一般来说矩阵乘向量确实想得到向量，这里很合理)
print(tf.linalg.matvec(a, b))   # [14], shape=(1,)

a = tf.constant(range(1, 4), shape=(1, 1, 3))
b = tf.constant(range(1, 4), shape=(1, 3))
# 这样也是可运行的，是先将内2层相乘，再套上最外层（一般用于批量相乘）
print(tf.linalg.matvec(a, b))   # [[14]], shape=(1, 1)

a = tf.constant(range(1, 4), shape=(1, 3))
b = tf.constant(range(1, 4), shape=(3, 1))
print(tf.tensordot(a, b, axes=0))
print(tf.tensordot(a, b, axes=1))
print(tf.tensordot(a, b, axes=2))
print(a @ b)                   # [[14]], shape=(1, 1)
# print(tf.matmul(a, b))  # 基本等价于上面的式子

n = np.arange(1, 4)
print(n @ n)  # 14


