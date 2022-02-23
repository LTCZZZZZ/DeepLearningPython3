# Cast Python arguments to Tensors to reduce retracing. Or force retracing.
#
# Often, Python arguments are used to control hyperparameters and graph constructions - for example,
# num_layers=10 or training=True or nonlinearity='relu'. So, if the Python argument changes,
# it makes sense that you'd have to retrace the graph.
#
# However, it's possible that a Python argument is not being used to control graph construction.
# In these cases, a change in the Python value can trigger needless retracing. Take, for example,
# this training loop, which AutoGraph will dynamically unroll. Despite the multiple traces,
# the generated graph is actually identical, so retracing is unnecessary.

import tensorflow as tf


def train_one_step():
    pass


@tf.function
def train(num_steps):
    print("Tracing with num_steps = ", num_steps)
    tf.print("Executing with num_steps = ", num_steps)
    for _ in tf.range(num_steps):
        train_one_step()


print("Retracing occurs for different Python arguments.")
train(num_steps=10)
train(num_steps=20)

print()
print("Traces are reused for Tensor arguments.")
train(num_steps=tf.constant(10))
train(num_steps=tf.constant(20))


# If you need to force retracing, create a new Function.
# Separate Function objects are guaranteed not to share traces.
def f():
    print('Tracing!')
    tf.print('Executing')


f1 = tf.function(f)  # 利用装饰器新生成一个函数，则必然会重新trace
f2 = tf.function(f)
f1()
f2()
