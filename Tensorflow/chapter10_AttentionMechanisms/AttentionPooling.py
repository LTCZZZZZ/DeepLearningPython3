# 10.2. Attention Pooling: Nadaraya-Watson Kernel Regression

import tensorflow as tf
from d2l import tensorflow as d2l

# 在使用同样随机数种子的情况下，每次执行生成的随机数结果相同
tf.random.set_seed(seed=1322)

n_train = 50
x_train = tf.sort(tf.random.uniform(shape=(n_train,), maxval=5))


def f(x):
    return 2 * tf.sin(x) + x ** 0.8


y_train = f(x_train) + tf.random.normal(
    (n_train,), 0.0, 0.5)  # Training outputs
x_test = tf.range(0, 5, 0.1)  # Testing examples
y_truth = f(x_test)  # Ground-truth outputs for the testing examples
n_test = len(x_test)  # No. of testing examples
print(n_test)


def plot_kernel_reg(y_hat):
    d2l.plot(x_test, [y_truth, y_hat], 'x', 'y', legend=['Truth', 'Pred'],
             xlim=[0, 5], ylim=[-1, 5])
    d2l.plt.plot(x_train, y_train, 'o', alpha=0.5)
    d2l.plt.show()


y_hat = tf.repeat(tf.reduce_mean(y_train), repeats=n_test)
plot_kernel_reg(y_hat)

# Shape of `X_repeat`: (`n_test`, `n_train`), where each row contains the
# same testing inputs (i.e., same queries)
X_repeat = tf.repeat(tf.expand_dims(x_train, axis=0), repeats=n_train, axis=0)
# Note that `x_train` contains the keys. Shape of `attention_weights`:
# (`n_test`, `n_train`), where each row contains attention weights to be
# assigned among the values (`y_train`) given each query
attention_weights = tf.nn.softmax(
    -(X_repeat - tf.expand_dims(x_train, axis=1)) ** 2 / 2, axis=1)
# Each element of `y_hat` is weighted average of values, where weights are attention weights
y_hat = tf.matmul(attention_weights, tf.expand_dims(y_train, axis=1))
plot_kernel_reg(y_hat)

d2l.show_heatmaps(
    tf.expand_dims(tf.expand_dims(attention_weights, axis=0), axis=0),
    xlabel='Sorted training inputs', ylabel='Sorted testing inputs')
d2l.plt.show()

# 10.2.4. Parametric Attention Pooling
X = tf.ones((2, 1, 4))
Y = tf.ones((2, 4, 6))
# tf.matmul(X, Y).shape

weights = tf.ones((2, 10)) * 0.1
values = tf.reshape(tf.range(20.0), shape=(2, 10))
tf.matmul(tf.expand_dims(weights, axis=1), tf.expand_dims(values, axis=-1)).numpy()


class NWKernelRegression(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.w = tf.Variable(initial_value=tf.random.uniform(shape=(1,)))

    def call(self, queries, keys, values, **kwargs):
        # For training queries are `x_train`. Keys are distance of taining data for each point. Values are `y_train`.
        # Shape of the output `queries` and `attention_weights`: (no. of queries, no. of key-value pairs)
        queries = tf.repeat(tf.expand_dims(queries, axis=1),
                            repeats=keys.shape[1], axis=1)
        self.attention_weights = tf.nn.softmax(
            -((queries - keys) * self.w) ** 2 / 2, axis=1)
        # Shape of `values`: (no. of queries, no. of key-value pairs)
        return tf.squeeze(
            tf.matmul(tf.expand_dims(self.attention_weights, axis=1),
                      tf.expand_dims(values, axis=-1)))


# Shape of `X_tile`: (`n_train`, `n_train`), where each column contains the
# same training inputs
X_tile = tf.repeat(tf.expand_dims(x_train, axis=0), repeats=n_train, axis=0)
# Shape of `Y_tile`: (`n_train`, `n_train`), where each column contains the
# same training outputs
Y_tile = tf.repeat(tf.expand_dims(y_train, axis=0), repeats=n_train, axis=0)
# Shape of `keys`: ('n_train', 'n_train' - 1)
keys = tf.reshape(X_tile[tf.cast(1 - tf.eye(n_train), dtype=tf.bool)],
                  shape=(n_train, -1))
# Shape of `values`: ('n_train', 'n_train' - 1)
values = tf.reshape(Y_tile[tf.cast(1 - tf.eye(n_train), dtype=tf.bool)],
                    shape=(n_train, -1))

net = NWKernelRegression()
loss_object = tf.keras.losses.MeanSquaredError()
optimizer = tf.keras.optimizers.SGD(learning_rate=0.5)
animator = d2l.Animator(xlabel='epoch', ylabel='loss', xlim=[1, 5])

for epoch in range(5):
    with tf.GradientTape() as t:
        loss = loss_object(y_train, net(x_train, keys, values)) / 2 * len(
            y_train)  # To be consistent with d2l book
    grads = t.gradient(loss, net.trainable_variables)
    optimizer.apply_gradients(zip(grads, net.trainable_variables))
    print(f'epoch {epoch + 1}, loss {float(loss):.6f}')
    animator.add(epoch + 1, float(loss))
d2l.plt.show()


# Shape of `keys`: (`n_test`, `n_train`), where each column contains the same
# training inputs (i.e., same keys)
keys = tf.repeat(tf.expand_dims(x_train, axis=0), repeats=n_test, axis=0)
# Shape of `value`: (`n_test`, `n_train`)
values = tf.repeat(tf.expand_dims(y_train, axis=0), repeats=n_test, axis=0)
y_hat = net(x_test, keys, values)
plot_kernel_reg(y_hat)

d2l.show_heatmaps(
    tf.expand_dims(tf.expand_dims(net.attention_weights, axis=0), axis=0),
    xlabel='Sorted training inputs', ylabel='Sorted testing inputs')
d2l.plt.show()
