import random
import tensorflow as tf
from d2l import tensorflow as d2l

# 1、生成数据集
# 2、读取数据集
# 3、初始化模型参数
# 4、定义模型
# 5、定义损失函数
# 6、定义优化算法
# 7、训练


# 生成数据集
def synthetic_data(w, b, num_examples):  # @save
    """生成 y = Xw + b + 噪声。"""
    # X = tf.zeros((num_examples, w.shape[0]))
    # X += tf.random.normal(shape=X.shape)
    X = tf.random.normal(shape=(num_examples, w.shape[0]))  # 如此生成的每个样本中的两个特征有什么关系？测了一下好像没什么特别的关系，感觉上像是先全局生成然后reshape了一下
    y = tf.matmul(X, tf.reshape(w, (-1, 1))) + b
    y += tf.random.normal(shape=y.shape, stddev=0.01)
    # y = tf.reshape(y, (-1, 1))  # 这一行没必要吧？？
    return X, y


n = 1000  # 样本数
true_w = tf.constant([2, -3.4])
true_b = 4.2
features, labels = synthetic_data(true_w, true_b, n)
print('features:', features[0], '\nlabel:', labels[0])

d2l.set_figsize((4, 3))
d2l.plt.scatter(features[:, 0].numpy(), labels.numpy(), 1, 'orange')
d2l.plt.scatter(features[:, 1].numpy(), labels.numpy(), 1)
# 可以看出图像的中心点大约为(0,4.2)，而橙色图像明显感觉比蓝色图像更宽，
# 因为同样的正态分布，所乘系数不同，2 < |-3.4|，橙色点所受的扰动绝对值为3.4，而蓝色点所受扰动的绝对值为2
d2l.plt.show()

# 读取数据集
def data_iter(batch_size, features, labels):
    # 此方法获取的各批次中，不会有重复的样本
    # 另外，这是一个迭代器
    num_examples = len(features)
    indices = list(range(num_examples))
    # 这些样本是随机读取的，没有特定的顺序
    random.shuffle(indices)  # 随机排序列表中的全部元素
    for i in range(0, num_examples, batch_size):
        j = tf.constant(indices[i:min(i + batch_size, num_examples)])  # 每个循环获取一批
        yield tf.gather(features, j), tf.gather(labels, j)  # 根据索引获取元素


batch_size = 10

# 当我们运行迭代时，我们会连续地获得不同的小批量，直至遍历完整个数据集。
# 上面实现的迭代对于教学来说很好，但它的执行效率很低，可能会在实际问题上陷入麻烦。
# 例如，它要求我们将所有数据加载到内存中，并执行大量的随机内存访问。
# 在深度学习框架中实现的内置迭代器效率要高得多，它可以处理存储在文件中的数据和通过数据流提供的数据。
# for X, y in data_iter(batch_size, features, labels):
#     print(X, '\n', y)
#     break

# 初始化模型参数
w = tf.Variable(tf.random.normal(shape=(2, 1), mean=0, stddev=0.01),
                trainable=True)
b = tf.Variable(tf.zeros(1), trainable=True)

# 定义模型
def linreg(X, w, b):  # @save
    """线性回归模型。"""
    return tf.matmul(X, w) + b


# 定义损失函数
def squared_loss(y_hat, y):  #@save
    """均方损失。"""
    return (y_hat - tf.reshape(y, y_hat.shape))**2 / 2


# 定义优化算法
def sgd(params, grads, lr, batch_size):  #@save
    """小批量随机梯度下降。"""
    for param, grad in zip(params, grads):
        param.assign_sub(lr * grad / batch_size)


# 我自定义的函数，
# 其实可以在这里除以n，那样就不用在更新参数时除以n了，但这里就需要多传一个参数，不过，n=len(X)
# 但后来发现，如果n很大的话，这样做在求梯度时会损失精度，故而放弃这种方法
def loss_func(X, y, w, b):
    # return tf.norm(y - linreg(X, w, b)) ** 2 / 2  # 这算出来是标量
    # return (y - linreg(X, w, b)) ** 2 / 2 / len(X)  # 这是向量，t.gradient的时候会自动相加
    return (y - linreg(X, w, b)) ** 2 / 2           # 这是向量，t.gradient的时候会自动相加


lr = 0.03
num_epochs = 3
net = linreg
loss = squared_loss

for epoch in range(num_epochs):
    for X, y in data_iter(batch_size, features, labels):
        with tf.GradientTape() as g:
            l = loss(net(X, w, b), y)  # `X`和`y`的小批量损失
        # 计算l关于[`w`, `b`]的梯度
        dw, db = g.gradient(l, [w, b])
        # 使用参数的梯度更新参数
        sgd([w, b], [dw, db], lr, batch_size)
    train_l = loss(net(features, w, b), labels)
    print(f'epoch {epoch + 1}, loss {float(tf.reduce_mean(train_l)):f}')
    print(float(tf.reduce_sum(train_l)))
    print(float(tf.reduce_sum(loss_func(features, labels, w, b))))
print(w, '\n', b)



# 下面是我自己的代码


# 学习率
w = tf.Variable(tf.random.normal(shape=(2, 1), mean=0, stddev=0.01),
                trainable=True)
b = tf.Variable(tf.zeros(1), trainable=True)
eta = 0.5
epoch = 1000

# 一次更新全部(不分批)
for i in range(epoch):
    with tf.GradientTape() as t:
        loss = loss_func(features, labels, w, b)
    dw, db = t.gradient(loss, [w, b])
    w.assign_sub(eta * dw / n)
    b.assign_sub(eta * db / n)
    # w.assign_sub(eta * dw)  # 在损失函数中除以了n，这里就不用除了，后来还是放弃这种方法，因为在求梯度时会损失精度
    # b.assign_sub(eta * db)
    if i in (0, epoch - 1):
        print(tf.reduce_sum(loss))
print(w, '\n', b)

# 分批训练
w = tf.Variable(tf.random.normal(shape=(2, 1), mean=0, stddev=0.01),
                trainable=True)
b = tf.Variable(tf.zeros(1), trainable=True)
eta = 0.15
epoch = 100
for i in range(epoch):
    for X, y in data_iter(batch_size, features, labels):
        with tf.GradientTape() as t:
            loss = loss_func(X, y, w, b)
        dw, db = t.gradient(loss, [w, b])
        w.assign_sub(eta * dw / batch_size)
        b.assign_sub(eta * db / batch_size)
        # w.assign_sub(eta * dw)
        # b.assign_sub(eta * db)
    if i in (0, epoch - 1):  # 这里和上面有些不同，这里在i=0打印的loss，就已经是更新了99次之后的loss了
        print(tf.reduce_sum(loss))
        print(tf.reduce_sum(loss_func(features, labels, w, b)))
print(w, '\n', b)

# n = 1000，batch_size = 10
# 从结果来看，不知为何，分批训练得到的结果要比不分批好得多
# 即使把不分批时的epoch改到10000，从结果来看也没有什么改善，
# 而分批时即使epoch为1，结果也相当不错（分批时每个epoch实际更新了100次参数）
# 后来发现，是因为w, b更新参数时没有除以n
# 加上之后，适当调整学习率，发现在更新参数次数相同的条件下，整批训练效果更好(实际想来确实应该如此，毕竟每次更新由全部特征影响)
# 并且，分批训练即使epoch和整批相同，结果也没有整批好，
# 思考总结：分批训练可以使参数迅速接近期望值，所以，其实可以这样
# 先分批训练一段，当损失函数降低到某种程度时，再整批训练













