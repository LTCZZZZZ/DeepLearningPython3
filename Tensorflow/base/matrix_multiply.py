import tensorflow as tf
import numpy as np

x = tf.reshape(tf.range(9), (3, 3))
y = tf.ones((3, 3), dtype='int32')
z = tf.ones(3, dtype='int32')
print(x, y)
print(tf.tensordot(x, y, axes=0))  # 注意这里的参数是axes，axes=0有点类似于笛卡尔积
print(tf.tensordot(x, y, axes=1))  # 此时即为矩阵乘法
print(tf.tensordot(x, y, axes=2))  # axes=2的情况，没看懂

print(np.dot(x, y), tf.linalg.matvec(x, y))  # 这两个结果不同，互为转置
print(np.dot(x, z), tf.linalg.matvec(x, z))  # 这两个结果相等（可能因为都是一维的）

# 标准的矩阵乘法，容不得不规范的格式，但是shape(1,3,3)可以乘(3,3,1)，也可以乘(3,1)
print(tf.matmul(x, y))
# print(tf.matmul(x, z))  # 会报错 has different ndims: [3,3] vs. [3]
print(tf.matmul(x, tf.reshape(z, (3, 1))))

print()
x2 = tf.reshape(x, (1, 3, 3))
y2 = tf.reshape(y, (3, 3, 1))
z2 = tf.reshape(z, (3, 1))
print(tf.matmul(x2, y))   # (1,3,3)
print(tf.matmul(x2, y2))  # (3,3,1)  这个结果，看了半天才看懂，详见函数的文档说明
print(tf.matmul(x2, z2))  # (1,3,1)
# 注意，此方法可用@代替
print(x2 @ y)
print(x2 @ y2)
print(x2 @ z2)

# 范数
u = tf.constant([3.0, -4.0])
print(tf.norm(u, ord=2))  # Supported values are `'fro'`, `'euclidean'`, `1`, `2`, `np.inf` and any positive real number yielding the corresponding p-norm
print(tf.norm(u, ord=1))

# 小结
# 标量、向量、矩阵和张量是线性代数中的基本数学对象。
#
# 向量泛化自标量，矩阵泛化自向量。
#
# 标量、向量、矩阵和张量分别具有零、一、二和任意数量的轴。
#
# 一个张量可以通过sum 和 mean沿指定的轴降低维度。
#
# 两个矩阵的按元素乘法被称为他们的哈达玛积。它与矩阵乘法不同。
#
# 在深度学习中，我们经常使用范数，如  𝐿1 范数、 𝐿2 范数和弗罗贝尼乌斯范数。
#
# 我们可以对标量、向量、矩阵和张量执行各种操作。

A = tf.reshape(tf.range(12, dtype=tf.float32), (3, 4))
print(A / tf.reduce_sum(A, axis=1, keepdims=True))  # 如果不加keepdims参数在tf中会报错，试了一下np中也会
print(A.numpy() / A.numpy().sum(axis=1, keepdims=True))
print(A * tf.reduce_sum(A, axis=1, keepdims=True))
print(A.numpy() * A.numpy().sum(axis=1, keepdims=True))
