# d = display not healthy(阳性)，h = healthy(健康)

d_h = 0.01  # 已知健康，检出阳性的概率
nd_h = 1 - d_h  # 已知健康，检出阴性的概率
d_nh = 1  # 已知不健康，检出阳性的概率
nd_nh = 1 - d_nh  # 已知不健康，检出阴性的概率

p = 0.0015  # 人群综合患病率

d = p * d_nh + (1 - p) * d_h  # 人群中检出阳性的概率
nh_d = p * d_nh / d  # 实际上是1 / (1 + (1-p)/p * d_h)
print(nh_d == 1 / (1 + (1-p)/p * d_h))

# 首先，经测试发现，如果d_h变大，则nh_d减小，这说明，(对健康人群的)检测越不准，你检测出阳性时患病的概率就越小(因为阳性的基数增大了)
# 而在上面的条件都不变时，如果d_h=0，(此时有d_nh=1的前提)则若检出阳性，则必然患病

# 在d_nh=1的前提的前提下，nh_d关于d_h的导函数
def derived(x):
    temp = (1 - p) / p
    return - temp / (1 + temp * x) ** 2

print(derived(0))
print(derived(0.01))


# 用梯度计算一下nh_d关于d_h的函数
import tensorflow as tf

d_h = tf.Variable(d_h, dtype=tf.float64)
with tf.GradientTape() as t:
    d = p * d_nh + (1 - p) * d_h  # 人群中检出阳性的概率
    nh_d = p * d_nh / d  # 实际上是1 / (1 + (1-p)/p * d_h)
grad = t.gradient(nh_d, d_h)

# 由于精度问题，float32且d_h = 0.01时，下面的结果为False
# 但若将d_h设置为float16或float64类型，结果为True
print('梯度:', grad, derived(d_h), grad == derived(d_h))

# d_h = 0时注意观察这一行，结论：Tensor和float比较大小时，会先将float转为Tensor，而不是相反
print(grad == -665.6666666666667, float(grad), float(grad) == derived(0))


