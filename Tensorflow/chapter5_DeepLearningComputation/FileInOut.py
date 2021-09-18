import numpy as np
import tensorflow as tf

# x = tf.range(4)
# np.save('x-file.npy', x)

# x2 = np.load('x-file.npy', allow_pickle=True)
# print(x2)

class MLP(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.flatten = tf.keras.layers.Flatten()
        self.hidden = tf.keras.layers.Dense(units=256, activation=tf.nn.relu)
        self.out = tf.keras.layers.Dense(units=10)

    def call(self, inputs):
        x = self.flatten(inputs)
        x = self.hidden(x)
        return self.out(x)

net = MLP()
X = tf.random.uniform((2, 20))
Y = net(X)

net.save_weights('mlp.params')

clone = MLP()
clone.load_weights('mlp.params')
Y_clone = clone(X)
print(Y_clone == Y)
