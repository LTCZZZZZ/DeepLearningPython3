import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import time
import gzip
import pickle

# plt.rcParams['font.family'] = ['STXingkai']  # 此字体显示负号不正常，需搭配下面的设置
# plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
plt.rcParams['font.family']=['STKaiti']  # 此字体能自动显示负号

f = gzip.open('mnist.pkl.gz', 'rb')
training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
f.close()

# 如果全0初始化，无论训练多少个epoch，每个神经元的w参数全部相同，反应在结果中就是net的W每一行都和第一行相同（W一列表示一个神经元）
# 这表示神经元对上一层的所有输入的权重都相同
initializer = tf.initializers.Zeros
# initializer = tf.initializers.RandomNormal(stddev=0.3)
net = tf.keras.Sequential()
# tf.identity，tf.nn.relu，tf.nn.sigmoid，tf.nn.softmax
net.add(tf.keras.layers.Dense(10, kernel_initializer=initializer, activation=tf.nn.softmax))
# net.add(tf.keras.layers.Dense(10, kernel_initializer=initializer, activation=tf.nn.sigmoid))

# 看看初始化后未训练之前net的准确率
print((tf.argmax(net(training_data[0]), axis=1).numpy() == training_data[1]).sum())
print((tf.argmax(net(test_data[0]), axis=1).numpy() == test_data[1]).sum())
pre_w = net.weights[0]

loss = tf.keras.losses.MeanSquaredError()  # 这个loss函数是mean(分量差平方相加再除以分量数，再对样本n取平均值)的，但没有除以2
# print(loss(np.zeros(3, dtype=float), np.array([0, 1, 2], dtype=float)))
# print(loss(np.ones(10) * 0.1 , np.eye(10)[0]))  # 受计算机精度影响会有额外的小数位溢出值
trainer = tf.keras.optimizers.SGD(learning_rate=1)

# 即使是单层网络，前50个epoch看不出来什么，300个epoch就很明显了
# 此外，使用 tf.function 计算图，可大幅提升训练速度
epochs = 150

# 每个epoch中有如下几步：
# 1. 正向传播一遍
# 2. 求loss
# 3. 求梯度grads
# 4. 对参数应用优化算法
X = training_data[0]
# y的前10个是[5 0 4 1 9 2 1 3 1 4]
y = np.eye(10)[training_data[1]]  # 根据标签快速生成one-hot编码
# print(y[:10])
# print(y.shape)  # (50000, 10)

train_acc = []
test_acc = []


# 计算图中print和tf.print的区别：print是在编译过程中执行的，所以无意义，想观察执行过程中变量的变化，使用tf.print
# 另可参见 https://stackoverflow.com/questions/57469673/tf-print-vs-python-print-vs-tensor-eval
# @tf.function(jit_compile=True)  # 显式地启用 TensorFlow 中的 XLA（线性代数加速）功能
# @tf.function()
def train_model():
    for i in tf.range(epochs):  # 特别注意：这里一定要用tf.range，否则编译会超级慢，且如果次数较大，还会编译失败
        with tf.GradientTape() as tape:
            y_hat = net(X, training=True)
            # print(y_hat[0])
            # tf.print(y_hat[0])  # 从这儿就能看出print和tf.print的区别
            l = loss(y_hat, y)
            grads = tape.gradient(l, net.trainable_variables)
            trainer.apply_gradients(zip(grads, net.trainable_variables))  # 注意这里的zip不能掉
        # tf.print('before epoch', i + 1, 'loss:', l)

        # 看测试集的数据准确率
        train_correct = np.sum(tf.argmax(net(training_data[0]), axis=1) == training_data[1])
        test_correct = np.sum(tf.argmax(net(test_data[0]), axis=1) == test_data[1])
        train_acc.append(train_correct / 50000)
        test_acc.append(test_correct / 10000)
        # tf.print(train_correct)
        # tf.print(test_correct)


time0 = time.time()
print(time0)
train_model()  # 经测试发现，执行的时候才会编译
print(time.time() - time0)
print('after  epoch', epochs, 'loss:', loss(net(X), y))  # 这里又计算了一遍loss
plt.plot(range(1, epochs + 1), train_acc, label='训练集')
plt.plot(range(1, epochs + 1), test_acc, label='测试集')
plt.legend()  # 显示图例
plt.grid()  # 显示网格
plt.show()

# print(net.summary())
# print(dir(net.layers[1]))
# print(net.layers[0].weights)
# print(net.layers[1].weights)
# print(net.layers[1].bias)
#
# for i in net.get_weights():
#     # print(i.shape)
#     print(i)

print(net.weights)
print((pre_w != net.weights[0]).numpy().sum())  # 等于0说明w未被训练，就要考察为什么
