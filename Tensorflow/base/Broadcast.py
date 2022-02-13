# 当你的其中一个操作数是一个具有单独维度(singular dimension)的张量的时候，
# TF会隐式地在它的单独维度方向填满(tile)，以确保和另一个操作数的形状相匹配。
# 所以，对一个[3,2]的张量和一个[3,1]的张量相加在TF中是合法的。
# （译者：这个机制继承自numpy的广播功能。其中所谓的单独维度就是一个维度为1，或者那个维度缺失）
import numpy as np
import tensorflow as tf

# 总结：机制是，维数首先会从较低阶数张量开始扩展，并且这种扩展(应该)只会加在前面(重要important)，
# 比如shape=(3,)能变成(2,3)，或更进一步的(4,2,3)，
# 第二步，两个张量维数相同后，再对比shape，对其中不相等的，为1的dim进行扩展

a = tf.constant([[1.], [2.]])
b = tf.constant([1., 2.])
s = a + b
assert s.shape == (2, 2)  # 在代码中增加向量shape的断言，不易出错且能同时充当代码的文档
c = tf.reduce_sum(s)
print(s)
print(c)
# 第一个张量的shape为[2, 1]，第二个张量的shape为[2,]。因为从较低阶数张量的第一个维度开始扩展，
# 所以应该将第二个张量扩展为shape=[2,2]，也就是值为[[1,2], [1,2]]。
# 第一个张量将会变成shape=[2,2]，其值为[[1, 1], [2, 2]]

a = tf.constant([[1.], [2.]])
b = tf.constant([1., 2., 3.])
s = a + b
c = tf.reduce_sum(s)
print(s)
print(c)
# 第一个张量的shape为[2, 1]，第二个张量的shape为[3,]。因为从较低阶数张量的第一个维度开始扩展，
# 所以应该将第二个张量扩展为shape=[2,3]，也就是值为[[1,2,3], [1,2,3]]。
# 第一个张量将会变成shape=[2,3]，其值为[[1, 1, 1], [2, 2, 2]]

a = tf.reshape(tf.range(24), shape=(4, 2, 3))
b = tf.constant([1, 2, 3, 4])
b = tf.reshape(b, (4, 1, 1))  # 如果是(4,1)就不行
b = tf.tile(b, [1, 2, 3])  # 按维度扩充
print(b)
print(a + b)

b = np.arange(4)
# np的tile功能比tf更强大，可以在b的dim小于给定shape的dim时使用
# 比如此例会自动将b的shape先扩展为(1,1,4)
b = np.tile(b, (4, 2, 1))
print(b)
