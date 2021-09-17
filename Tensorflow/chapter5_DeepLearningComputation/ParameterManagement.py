import tensorflow as tf
import copy

# tf.keras的表现有点不同。它会自动删除重复层
shared = tf.keras.layers.Dense(4, activation=tf.nn.relu)
# tensorflow搞两个一样的层好像还很难做到
# shared_copy = copy.copy(shared)
# shared_copy.name = 'copy'
net = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    shared,
    shared,
    # shared_copy,
    tf.keras.layers.Dense(1),
])

X = tf.random.uniform((2, 4))
net(X)
# 检查参数是否不同
print(len(net.layers))
print(len(net.layers) == 3)
