# 6.4. Multiple Input and Multiple Output Channels
import tensorflow as tf
from d2l import tensorflow as d2l


def corr2d_multi_in(X, K):
    # 先遍历 “X” 和 “K” 的第0个维度（通道维度），再把它们加在一起
    return tf.reduce_sum([d2l.corr2d(x, k) for x, k in zip(X, K)], axis=0)


def corr2d_multi_in_out(X, K):
    # 迭代“K”的第0个维度，每次都对输入“X”执行互相关运算。
    # 最后将所有结果都叠加在一起
    return tf.stack([corr2d_multi_in(X, k) for k in K], 0)


def corr2d_multi_in_out_1x1(X, K):
    c_i, h, w = X.shape
    c_o = K.shape[0]
    X = tf.reshape(X, (c_i, h * w))
    K = tf.reshape(K, (c_o, c_i))
    # 全连接层中的矩阵乘法
    Y = tf.matmul(K, X)
    return tf.reshape(Y, (c_o, h, w))


X = tf.random.normal((3, 3, 3), 0, 1)
K = tf.random.normal((2, 3, 1, 1), 0, 1)

Y1 = corr2d_multi_in_out_1x1(X, K)
Y2 = corr2d_multi_in_out(X, K)
print(float(tf.reduce_sum(tf.abs(Y1 - Y2))))
assert float(tf.reduce_sum(tf.abs(Y1 - Y2))) < 1e-6
