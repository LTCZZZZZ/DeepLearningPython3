import tensorflow as tf

print(tf.constant(3))
print(tf.constant([3, 4.0]))

x = tf.reshape(tf.range(12), (3, 4))
print(x)
print(x[0, 1])
print(x.shape, len(x), tf.size(x))  # 形状，长度，size，注意size返回的是Tensor对象
# axis=m的意思是，在取元素时，每次固定非m轴，然后遍历第m轴得到的元素作为一组来计算(m轴除外后的shape相乘为组的数量)，
# 得到结果的shape是原shape将m轴除外后的shape
print(tf.reduce_sum(x), tf.reduce_sum(x, 0), tf.reduce_sum(x, 1))

print(tf.transpose(x))
tf.reshape(x, (3, 4))

tf.reduce_sum(x)

tf.zeros((3, 4))

# tf.random.set_seed(5)
tf.random.normal([3, 4])  # 注意seed参数

tf.constant([[2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])

tf.cast(x, tf.float32)  # 类型转换


X = tf.reshape(tf.range(12, dtype=tf.float32), (3, 4))
Y = tf.constant([[2.0, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
print(X, Y)
tf.concat([X, Y], axis=0)  # 增加行
tf.concat([X, Y], axis=1)  # 增加列

# 广播，大多数情况下，会沿着数组中长度为1的轴进行广播
a = tf.reshape(tf.range(3), (3, 1))
b = tf.reshape(tf.range(2), (1, 2))
a + b

# TensorFlow中的 Tensors 是不可变的，也不能被赋值。
# TensorFlow中的 Variables 是支持赋值的可变容器。
# 请记住，TensorFlow中的梯度不会通过 Variable 反向传播。————这里暂时没看懂，没懂
X_var = tf.Variable(X)
X_var[1, 2].assign(9)
X_var
# 如果我们想为多个元素赋值相同的值，我们只需要索引所有元素，然后为它们赋值。
X_var = tf.Variable(X)
X_var[0:2, :].assign(tf.ones(X_var[0:2, :].shape, dtype=tf.float32) * 12)
X_var

# Variables 是TensorFlow中的可变容器。它们提供了一种存储模型参数的方法。
Z = tf.Variable(tf.zeros_like(Y))
print('id(Z):', id(Z))
Z.assign(X + Y)
print('id(Z):', id(Z))  # Z的id不变

# 由于 TensorFlow的 Tensors 是不可变的，而且梯度不会通过 Variable 流动，
# 因此 TensorFlow 没有提供一种明确的方式来原地运行单个操作。
# 但是，TensorFlow提供了tf.function修饰符，将计算封装在TensorFlow图中，该图在运行前经过编译和优化。
# 这允许TensorFlow删除未使用的值，并复用先前分配的且不再需要的值。这样可以最大限度地减少 TensorFlow 计算的内存开销。

# 这里基本没看懂，此外，python这种脚本执行的方式，如何在运行前编译和优化？
# 难道执行到这儿的时候停下来编译吗？或是在开始执行前先全局检测然后编译？
@tf.function
def computation(X, Y):
    Z = tf.zeros_like(Y)  # 这个未使用的值将被删除
    A = X + Y  # 当不再需要时，分配将被复用
    B = A + Y
    C = B + Y
    return C + Y

computation(X, Y)

# 转换为其他 Python 对象
A = X.numpy()
B = tf.constant(A)
type(A), type(B)
