import time

import numpy as np
import json

from matplotlib import pyplot as plt


def load_data():
    # 从文件导入数据
    datafile = './work/housing.data'
    data = np.fromfile(datafile, sep=' ')
    print(data.shape)  # (7084,)

    # 读入之后的数据被转化成1维array，其中array的第0-13项是第一条数据，第14-27项是第二条数据，以此类推....
    # 这里对原始数据做reshape，变成N x 14的形式
    feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS',
                     'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
    feature_num = len(feature_names)
    data = data.reshape([data.shape[0] // feature_num, feature_num])

    # 将原数据集拆分成训练集和测试集
    # 这里使用80%的数据做训练，20%的数据做测试
    # 测试集和训练集必须是没有交集的
    ratio = 0.8
    offset = int(data.shape[0] * ratio)
    training_data = data[:offset]
    print(training_data.shape),  # (404, 14)

    # 对每个特征进行归一化处理，使得每个特征的取值缩放到0~1之间。这样做有两个好处：
    # 一是模型训练更高效；
    # 二是特征前的权重大小可以代表该变量对预测结果的贡献度（因为每个特征值本身的范围相同）。
    # 计算train数据集的最大值，最小值
    # 注意：思考一下为什么要使用训练数据集的最大值和最小值，而不是整个数据集的最大值和最小值？
    # 答：因为假如模型要投入到实际应用中，对新数据的最大值和最小值是未知的
    maximums, minimums = training_data.max(axis=0), training_data.min(axis=0)
    # print(maximums, minimums)
    # 对数据进行归一化处理

    # 可以验证，下面两种方式是等价的
    # data1 = data.copy()
    # for i in range(feature_num):
    #     data1[:, i] = (data[:, i] - minimums[i]) / (maximums[i] - minimums[i])
    # data2 = (data - minimums) / (maximums - minimums)
    # print(np.all(data1 == data2))

    # # 利用广播机制，这里可以写得更简单，上面被注释的代码验证了这一点
    data = (data - minimums) / (maximums - minimums)

    # 训练集和测试集的划分比例
    training_data = data[:offset]
    test_data = data[offset:]
    return training_data, test_data


# 获取数据
training_data, test_data = load_data()
# x = training_data[:, :-1]
# y = training_data[:, -1:]


class Network(object):
    def __init__(self, num_of_weights):
        # 随机产生w的初始值

        # 为了保持程序每次运行结果的一致性，
        # 此处设置固定的随机数种子
        # np.random.seed(0)

        self.w = np.random.randn(num_of_weights, 1)
        self.b = 0.
        self.z = 0.

    def forward(self, x):
        z = np.dot(x, self.w) + self.b
        self.z = z
        return z

    def loss(self, y, z=None):
        if z is None:
            z = self.z
        cost = np.mean((z - y) ** 2)
        return cost

    def gradient(self, x, y):
        z = self.forward(x)
        gradient_w = (z - y) * x
        # print('gradient_w shape {}'.format(gradient_w.shape))  # (404, 13)
        # print(gradient_w)
        gradient_w = np.mean(gradient_w, axis=0)
        # print('gradient_w shape', gradient_w.shape)  # (13,)
        gradient_w = gradient_w[:, np.newaxis]  # 这种操作我之前还真没见过，新增一个axis
        # print('gradient_w shape', gradient_w.shape)  # (13, 1)
        gradient_b = (z - y)
        gradient_b = np.mean(gradient_b)

        return gradient_w, gradient_b

    def update(self, gradient_w, gradient_b, eta=1e-2):
        self.w = self.w - eta * gradient_w
        self.b = self.b - eta * gradient_b

    def train(self, training_data, epoch=1e5, batch_size=50):
        n = len(training_data)
        epochs = []
        losses = []
        time_cost = []
        eta = 1e-2
        for i in range(int(epoch)):
            # 学习率渐进式减小的策略
            if i >= 2e4:
                eta = 1e-3
            elif i >= 5e4:
                eta = 1e-4
            time0 = time.time()
            # 将数据乱序，洗牌
            np.random.shuffle(training_data)
            mini_batches = [training_data[k:k + batch_size] for k in range(0, n, batch_size)]
            for iter_id, mini_batch in enumerate(mini_batches):
                x = mini_batch[:, :-1]
                y = mini_batch[:, -1:]
                gradient_w, gradient_b = self.gradient(x, y)
                self.update(gradient_w, gradient_b, eta=eta)

            if i % 1e4 == 0:
                # print('time cost: {}'.format(time.time() - time0))
                print('epoch: {}, loss: {}'.format(i, self.loss(y)))

                # 可以看到，超过10000个epoch后，哪怕loss在训练集上仍有下降的趋势，但是在测试集上却基本不变了
                print('evaluate:', net.loss(test_data[:, -1:], z=net.forward(test_data[:, :-1])))

            if i % 1e3 == 0:
                epochs.append(i)
                losses.append(self.loss(training_data[:, -1:], z=self.forward(training_data[:, :-1])))
                time_cost.append(time.time() - time0)

        # 画出损失函数的变化趋势
        plt.plot(epochs, losses, color='r', label='loss')
        plt.plot(epochs, time_cost, color='b', label='time cost')
        plt.xlabel('epoch')
        plt.show()


# # 此处可以一次性计算多个样本的预测值和损失函数
# net = Network(13)
# x1 = x[0:3]
# y1 = y[0:3]
# z = net.forward(x1)
# print('predict: ', z)
# loss = net.loss(z, y1)
# print('loss:', loss)

net = Network(13)
print(net.forward(training_data[:, :-1]).shape)  # (404, 1)
# z = net.forward(x)
# loss = net.loss(z, y)
# gradient_w, gradient_b = net.gradient(x, y)
# print('loss:', loss)
# print('gradient_w:', gradient_w)

net.train(training_data)
print('loss:', net.loss(training_data[:, -1:], z=net.forward(training_data[:, :-1])))
print('evaluate:', net.loss(test_data[:, -1:], z=net.forward(test_data[:, :-1])))


# SGD（Stochastic Gradient Descent），随机梯度下降，
# 通过大量实验发现，模型对最后出现的数据印象更加深刻。
# 训练数据导入后，越接近模型训练结束，最后几个批次数据对模型参数的影响越大。
# 为了避免模型记忆影响训练效果，需要进行样本乱序操作。

# 在两层循环的内部是经典的四步训练流程：前向计算->计算损失->计算梯度->更新参数
