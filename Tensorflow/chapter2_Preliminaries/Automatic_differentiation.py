import tensorflow as tf

x = tf.range(4, dtype=tf.float32)
print(type(x))  # tensorflow.python.framework.ops.EagerTensor
print(len(x))  # 4

x = tf.Variable(x)
print(type(x))  # tensorflow.python.ops.resource_variable_ops.ResourceVariable
# print(len(x))  # object of type 'ResourceVariable' has no len()
print(tf.sin(x))
print(type(tf.sin(x)))

# Record all computations onto a tape
with tf.GradientTape(persistent=True) as t:
    # t.watch(x)
    y = 2 * tf.tensordot(x, x, axes=1)
    z = tf.reduce_sum(x)
x_grad = t.gradient(y, x)
print(x_grad, x_grad == 4 * x)  # 思考：梯度具体是怎样计算的？它为何能在精度上达到与4 * x相等？
print(t.gradient(y, x))

print(t.gradient(z, x))

# 例子中的watch函数把需要计算梯度的变量x加进来了。GradientTape默认只监控由tf.Variable创建的traiable=True属性（默认）的变量。
# 如果x是constant，则梯度需要增加t.watch(x)函数。当然，也可以设置不自动监控可训练变量，完全由自己指定，
# 设置watch_accessed_variables=False就行了（一般用不到）。

# 另外，默认情况下GradientTape的资源在调用gradient函数后就被释放，再次调用就无法计算了。
# 所以如果需要多次计算梯度，需要开启persistent=True属性

with tf.GradientTape() as t:
    y = x * x
    # y = tf.reduce_sum(x * x)  # 和上面的相比，求梯度的结果相同
    print(y)
print(t.gradient(y, x))

# 有时，我们希望将某些计算移动到记录的计算图之外。 例如，假设y是作为x的函数计算的，而z则是作为y和x的函数计算的。
# 现在，想象一下，我们想计算 z 关于 x 的梯度，但由于某种原因，我们希望将 y 视为一个常数，并且只考虑到 x 在y被计算后发挥的作用。
# 在这里，我们可以分离 y 来返回一个新变量 u，该变量与 y 具有相同的值，但丢弃计算图中如何计算 y 的任何信息。
# 换句话说，梯度不会向后流经 u 到 x。因此，下面的反向传播函数计算 z = u * x 关于 x 的偏导数，同时将 u 作为常数处理，而不是z = x * x * x关于 x 的偏导数。
with tf.GradientTape(persistent=True) as t:
    y = x * x
    # u = y
    u = tf.stop_gradient(y)
    z = u * x

x_grad = t.gradient(z, x)
print(x_grad, x_grad == u)
print(t.gradient(y, x) == 2 * x)


def f(a):
    b = a * 2
    while tf.norm(b) < 1000:
        b = b * 2
    if tf.reduce_sum(b) > 0:
        c = b
    else:
        c = 100 * b
    return c


a = tf.Variable(tf.random.normal(shape=()))
# tf.print(a)  # 貌似会用红色显示打印
print(a)
with tf.GradientTape() as t:
    d = f(a)
d_grad = t.gradient(d, a)
print(d_grad, d_grad == d / a)


# 看看y=Ax的导数是分子布局还是分母布局
x = tf.Variable([[1], [2]], dtype=float)
A = tf.constant(range(6, 10), dtype=float, shape=(2, 2))
with tf.GradientTape(persistent=True) as t:
    # y = tf.linalg.matvec(A, x)
    y = A @ x
    print(y)
    y_sum = tf.reduce_sum(y)
print(t.gradient(y, x))  # 可以看出此结果的shape始终与x相同，并非一般意义上的梯度，至于具体是怎么算的，以及有什么用，后续待察
print(t.batch_jacobian(y, x))
print(t.jacobian(y, x))  # 详见文档
# 后面发现，至少对一维的y来说，gradient(y, x)和gradient(y_sum, x)相等
print(t.gradient(y_sum, x))

