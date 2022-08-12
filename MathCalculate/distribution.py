from scipy.stats import binom
import matplotlib.pyplot as plt
import seaborn

seaborn.set()

# 二项分布
fig, ax = plt.subplots(3, 1)
params = [(10, 0.25), (10, 0.5), (10, 0.8)]
x = range(0, 11)

for i in range(len(params)):
    binom_rv = binom(n=params[i][0], p=params[i][1])
    ax[i].set_title('n={},p={}'.format(params[i][0], params[i][1]))
    ax[i].plot(x, binom_rv.pmf(x), 'bo', ms=8)
    ax[i].vlines(x, 0, binom_rv.pmf(x), colors='b', lw=3)
    ax[i].set_xlim(0, 10)
    ax[i].set_ylim(0, 0.35)
    ax[i].set_xticks(x)
    ax[i].set_yticks([0, 0.1, 0.2, 0.3])

plt.show()

# 几何分布
from scipy.stats import geom

fig, ax = plt.subplots(3, 1)
params = [0.5, 0.25, 0.1]
x = range(1, 11)

for i in range(len(params)):
    geom_rv = geom(p=params[i])
    ax[i].set_title('p={}'.format(params[i]))
    ax[i].plot(x, geom_rv.pmf(x), 'bo', ms=8)
    print(sum(geom_rv.pmf(x)))  # 0.1的话，10次内能成功的概率为65%，你觉得是高还是低呢？
    ax[i].vlines(x, 0, geom_rv.pmf(x), colors='b', lw=5)
    ax[i].set_xlim(0, 10)
    ax[i].set_ylim(0, 0.6)
    ax[i].set_xticks(x)
    ax[i].set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])

plt.show()

# 泊松分布
from scipy.stats import poisson

fig, ax = plt.subplots(3, 1)
x = range(0, 20)
params = [10, 3, 3.5]

for i in range(len(params)):
    poisson_rv = poisson(mu=params[i])
    mean, var, skew, kurt = poisson_rv.stats(moments='mvsk')
    ax[i].plot(x, poisson_rv.pmf(x), 'bo', ms=8)
    print(poisson_rv.pmf(x))
    ax[i].vlines(x, 0, poisson_rv.pmf(x), colors='b', lw=5)
    ax[i].set_title('$\\lambda$={}'.format(params[i]))
    ax[i].set_xticks(x)
    print('lambda={},E[X]={},V[X]={}'.format(params[i], mean, var))

plt.show()
