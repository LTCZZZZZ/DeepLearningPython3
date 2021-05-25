import math
import numpy as np
import tensorflow as tf
from d2l import tensorflow as d2l
from tools import Timer

n = 10000
a = tf.ones(n)
b = tf.ones(n)

c = tf.Variable(tf.zeros(n))
# c = [0 for i in range(10000)]
# a = [1 for i in range(10000)]
timer = Timer()
# for i in range(n):
#     # c[i] = a[i] + a[i]  # 但是不用tf数据格式而用python自带的列表的话，会快很多，大约只需0.0002s左右
#     # (a[i] + b[i])  # 可尝试不赋值，只看取值的耗时，结果说明tf的Tensor结构不论是取值还是赋值都很慢，比python的list要慢很多
#     c[i].assign(a[i] + b[i])
# print(f'{timer.stop():.6f} sec')

timer.start()
d = a + b
print(f'{timer.stop():.6f} sec')

print(math.pi)

d2l.plt()
