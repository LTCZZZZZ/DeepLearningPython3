import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from d2l import tensorflow as d2l

fair_probs = tf.ones(6) / 6
sample = tfp.distributions.Multinomial(1, fair_probs).sample()
# print(sample)

sample = tfp.distributions.Multinomial(1000, fair_probs).sample()
print(sample / 1000)

counts = tfp.distributions.Multinomial(10, fair_probs).sample(500)

# 逐行向下累加
cum_counts = tf.cumsum(counts, axis=0)

# 使得每一行都除以自己那一行数字的和
estimates = cum_counts / tf.reduce_sum(cum_counts, axis=1, keepdims=True)  # 注意这一行的计算，有一定的技巧性，用到了keepdims

d2l.set_figsize((6, 4.5))
for i in range(6):
    # 其实这个需要优化，这里第一组数据对应的x为0，其实应该为1合理一点
    # d2l.plt.plot(estimates[:3, i].numpy(), label=("P(die=" + str(i + 1) + ")"))
    d2l.plt.plot(estimates[:, i].numpy(), label=("P(die=" + str(i + 1) + ")"))
d2l.plt.axhline(y=0.167, color='black', linestyle='dashed')
d2l.plt.gca().set_xlabel('Groups of experiments')
d2l.plt.gca().set_ylabel('Estimated probability')
d2l.plt.legend()
d2l.plt.show()
