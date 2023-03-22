import paddle
from paddle.nn import Linear
import paddle.nn.functional as F
import numpy as np
import os
import random


# paddle.nn.functional：与paddle.nn一样，包含组网相关的API，如：Linear、激活函数ReLU等，
# 二者包含的同名模块功能相同，运行性能也基本一致。
# 差别在于paddle.nn目录下的模块均是类，每个类自带模块参数；paddle.nn.functional目录下的模块均是函数，需要手动传入函数计算所需要的参数。
# 在实际使用时，卷积、全连接层等本身具有可学习的参数，建议使用paddle.nn；
# 而激活函数、池化等操作没有可学习参数，可以考虑使用paddle.nn.functional


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


class Regressor(paddle.nn.Layer):

    def __init__(self):
        # 初始化父类中的一些参数
        super(Regressor, self).__init__()

        # 定义一层全连接层，输入维度是13，输出维度是1
        self.fc = Linear(in_features=13, out_features=1)

    # 网络的前向计算
    def forward(self, inputs):
        x = self.fc(inputs)
        return x


# 声明定义好的线性回归模型
model = Regressor()
# 开启模型训练模式
model.train()
# 加载数据
training_data, test_data = load_data()
# 定义优化算法，使用随机梯度下降SGD
# 学习率设置为0.01
opt = paddle.optimizer.SGD(learning_rate=0.01, parameters=model.parameters())
# 感觉这里opt有点类似于TensorFlow中的tf.GradientTape()，应该会自动记录parameters的梯度信息

EPOCH_NUM = 10  # 设置外层循环次数
BATCH_SIZE = 10  # 设置batch大小

# 定义外层循环
# for epoch_id in range(EPOCH_NUM):
#     # 在每轮迭代开始之前，将训练数据的顺序随机的打乱
#     np.random.shuffle(training_data)
#     # 将训练数据进行拆分，每个batch包含10条数据
#     mini_batches = [training_data[k:k + BATCH_SIZE] for k in range(0, len(training_data), BATCH_SIZE)]
#     # 定义内层循环
#     for iter_id, mini_batch in enumerate(mini_batches):
#         x = np.array(mini_batch[:, :-1])  # 获得当前批次训练数据
#         y = np.array(mini_batch[:, -1:])  # 获得当前批次训练标签（真实房价）
#         # 将numpy数据转为飞桨动态图tensor的格式
#         house_features = paddle.to_tensor(x, dtype='float32')
#         prices = paddle.to_tensor(y, dtype='float32')
#
#         # 前向计算
#         predicts = model(house_features)
#
#         # 计算损失
#         loss = F.square_error_cost(predicts, label=prices)
#         avg_loss = paddle.mean(loss)
#         if iter_id % 20 == 0:
#             print("epoch: {}, iter: {}, loss is: {}".format(epoch_id, iter_id, avg_loss.numpy()))
#
#         # 反向传播，计算每层参数的梯度值
#         avg_loss.backward()
#         # 更新参数，根据设置好的学习率迭代一步
#         opt.step()
#         # 清空梯度变量，以备下一轮计算
#         opt.clear_grad()


# 以下是高层API
paddle.set_default_dtype("float32")

train_dataset = paddle.text.datasets.UCIHousing(mode='train')
eval_dataset = paddle.text.datasets.UCIHousing(mode='test')
print(len(eval_dataset))

# 训练模型
model = paddle.Model(Regressor())
model.prepare(paddle.optimizer.SGD(learning_rate=0.005, parameters=model.parameters()),
              paddle.nn.MSELoss())
model.fit(train_dataset, eval_dataset, epochs=10, batch_size=8, verbose=1)

result = model.evaluate(eval_dataset, batch_size=8)
print("result:", result)

idx = np.random.randint(0, len(eval_dataset))
one_data, label = eval_dataset[idx]
one_data = one_data.reshape([1, -1])  # # 修改该条数据shape为[1,13]
print("index: {}, data: {}, label: {}".format(idx, one_data, label))
result_pred = model.predict(one_data, batch_size=1)  # result_pred是一个list，元素数目对应模型的输出数目
result_pred = result_pred[0]  # tuple,其中第一个值是个array
print("Inference result is {}, the corresponding label is {}".format(result_pred[0][0], label))
