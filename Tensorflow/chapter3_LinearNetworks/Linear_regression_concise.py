# net会(逐层)计算 X=tf.matmul(X, W) + b，相当于X在最左边，然后每层右乘矩阵W，再加b，进入下一层
# X的行数表示样本数n，列数m表示特征数，每次乘完后行数n不变，
# W为w(列向量，维数为m，每个分量会作用于X的一个特征)的组合，每个w表示一个神经元对特征的映射，得出的结果作为下一层的特征输入，
# 即这一层W中w的个数(W的列数)=下一层输入X的特征数(X的列数)
import numpy as np
import tensorflow as tf
from d2l import tensorflow as d2l

true_w = tf.constant([2, -3.4])
true_w = tf.reshape(true_w, shape=(-1, 1))  # 按照上面的注释，w真正应该具有的形状
true_b = 4.2
features, labels = d2l.synthetic_data(true_w, true_b, 1000)


def load_array(data_arrays, batch_size, is_train=True):  # @save
    """构造一个TensorFlow数据迭代器。"""
    # 对于此函数来说，列表会被视为单个component转成tensor对象，但元组不会
    # 所以，如果要传入多个对象，使用元组将它们组合起来
    dataset = tf.data.Dataset.from_tensor_slices(data_arrays)
    if is_train:
        # Randomly shuffles the elements of this dataset.
        # This dataset fills a buffer with buffer_size elements, then randomly samples elements
        # from this buffer, replacing the selected elements with new elements.
        # For perfect shuffling, a buffer size greater than or equal to the full size of the dataset is required.
        # For instance, if your dataset contains 10,000 elements but buffer_size is set to 1,000,
        # then shuffle will initially select a random element from only the first 1,000 elements in the buffer.
        # Once an element is selected, its space in the buffer is replaced by the next (i.e. 1,001-st) element,
        # maintaining the 1,000 element buffer.
        dataset = dataset.shuffle(buffer_size=1000)
        # 只有在实际访问数据时才会执行shuffle，故而如果每次打印list(dataset)，结果可能不同
        # 可以用iter(dataset)获取到迭代器
    dataset = dataset.batch(batch_size)  # 按batch_size切分
    return dataset


batch_size = 10
data_iter = load_array((features, labels), batch_size)  # data_iter是一个随机迭代器，只有实际迭代时才会进行shuffle等计算

# 定义模型同时初始化模型参数
# `keras` 是TensorFlow的高级API
initializer = tf.initializers.RandomNormal(stddev=0.01)
net = tf.keras.Sequential()
net.add(tf.keras.layers.Dense(3, kernel_initializer=initializer))  # 这里添加一个全连接层（自动包含w,b）
net.add(tf.keras.layers.Dense(1, kernel_initializer=initializer))  # 再添加一个全连接层（这里）
# 在后端执行时，初始化实际上是 推迟 （deferred）执行的。
# 只有在我们第一次尝试通过网络传递数据时才会进行真正的初始化。只是要记住，因为参数还没有初始化，所以我们不能访问或操作它们。

# 定义损失函数
# loss = tf.keras.losses.Huber() # 不知为何在2层时此函数表现较好，1层时MeanSquaredError更好
loss = tf.keras.losses.MeanSquaredError()  # 这个loss函数是mean(对样本n取平均值)的
# 经过下面与Linear_regression_scratch.py中squared_loss的比较，此loss函数是没有除以2的

# 定义优化算法
trainer = tf.keras.optimizers.SGD(learning_rate=0.03)

def squared_loss(y_hat, y):  #@save
    """均方损失。"""
    return (y_hat - tf.reshape(y, y_hat.shape))**2 / 2

# 训练
num_epochs = 3
for epoch in range(num_epochs):
    # 三次迭代，每次data_iter中数据的顺序都不相同
    for X, y in data_iter:
        with tf.GradientTape() as tape:
            l = loss(net(X, training=True), y)
        grads = tape.gradient(l, net.trainable_variables)  # 求梯度
        trainer.apply_gradients(zip(grads, net.trainable_variables))  # 更新参数
    l = loss(net(features), labels)
    print(f'epoch {epoch + 1}, loss {l:f}')
    # print(tf.reduce_mean(squared_loss(net(features), labels)))  # 是上面结果的1/2

# 网络概要
print(net.summary())
# 也可以这样获取参数
print(net.layers[1].weights)
# 上面添加了两个全连接层
print(net.get_weights())
for i in net.get_weights():
    print(i.shape)

# w = net.get_weights()[0]
# print('w的估计误差：', true_w)
# b = net.get_weights()[1]
# print('b的估计误差：', true_b - b)
