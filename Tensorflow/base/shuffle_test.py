import tensorflow as tf

d = tf.data.Dataset.from_tensor_slices(range(1, 11))
# d = d.batch(2).shuffle(10)
d = d.shuffle(10).batch(2)
print(list(d.as_numpy_iterator()))

