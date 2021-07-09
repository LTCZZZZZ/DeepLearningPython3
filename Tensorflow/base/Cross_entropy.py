import numpy as np
import tensorflow as tf


def cross_entropy(y, y_hat):
    """对每个样本求交叉熵，加起来再平均。这里是一次全部sum(单样本求交叉熵的过程中也有sum操作)再除以样本数"""
    return -np.sum(y * np.log(y_hat)) / len(y)


def multiple_cross_entropy(y, y_hat):
    """将每个样本的每个分量视为二项分布求交叉熵，相加得到样本的交叉熵，再对样本平均，
    一般用于多标签分类的情况"""
    return -np.sum(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat)) / len(y)


mse = tf.keras.losses.MeanSquaredError()  # 不仅会对样本数平均，对分量数也会平均


# 真实值
y = np.array([[0, 0, 1],
              [0, 1, 0],
              [1, 0, 0]])

y3 = np.array([[1, 0, 1],
              [0, 1, 0],
              [1, 0, 0]], dtype=float)  # 得加float，否则与y计算会局限于整数范围内

# net1估计值
y1 = np.array([[0.3, 0.3, 0.4],
               [0.3, 0.4, 0.3],
               [0.1, 0.2, 0.7]])

# net2估计值
y2 = np.array([[0.1, 0.2, 0.7],
               [0.1, 0.7, 0.2],
               [0.3, 0.4, 0.3]])


print((loss1 := cross_entropy(y, y1)))
print((m_loss1 := multiple_cross_entropy(y, y1)))
print((loss2 := cross_entropy(y, y2)))
print((m_loss2 := multiple_cross_entropy(y, y2)))

print(mse(y, y1))
print(mse(y, y2))
print(mse(y, y3))


