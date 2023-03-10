import numpy as np
import json


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
x = training_data[:, :-1]
y = training_data[:, -1:]
