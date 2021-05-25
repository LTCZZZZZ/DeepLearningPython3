import matplotlib.pyplot as plt
import numpy as np

n1 = [0, 1, 2, 3, 4]
m1 = [2, 3, -1, 1, -2]
n2 = [0, 1, 2, 3, 4]
m2 = [1, 1, 1, 1, 1]
plt.plot(n1, m1, 'r-.p', n2, m2,  'g-..')  # 此种只对紧跟的曲线生效
plt.plot(n1, m1, n2, m2, color='b')  # 此种对前面的所有曲线生效
# 参见 https://zhuanlan.zhihu.com/p/110656183
plt.show()

n = np.linspace(-5, 4, 30)

m1 = 3 * n + 2  # 二元一次方程，即直线
m2 = n ** 2  # 二元二次方程，即抛物线

plt.plot(n, m1, 'r-.', n, m2, 'b')

# 范围
plt.xlim((-2, 4))  #将X轴范围设定在(-2, 4)
plt.ylim((-5, 15))  #将Y轴范围设定在(-5, 15)

# 刻度，与范围二取其一
x_ticks = np.linspace(-5, 4, 10)  # 产生区间在-5至4间的10个均匀数值
plt.xticks(x_ticks)  # 将linspace产生的新的十个值传给xticks( )函数，用以改变坐标刻度，这行如果在plt.xlim之前，会失效

# 将对应标度位置的数字替换为想要替换的字符串，其余为替换的不再显示
plt.yticks([-2.5, 7.5], ['hate','love'])

# 标签
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.xlabel('X轴')
plt.ylabel('Y轴')

plt.show()
