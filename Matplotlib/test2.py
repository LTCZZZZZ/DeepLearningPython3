import matplotlib.pyplot as plt
import numpy as np

n1 = [0, 1, 2, 3, 4]
m1 = [2, 3, -1, 1, -2]
n2 = [0, 1, 2, 3, 4]
m2 = [1, 1, 1, 1, 1]
plt.plot(n1, m1, 'r-.p', n2, m2,  'g-..')  # 此种只对紧跟的曲线生效
line1, line2 = plt.plot(n1, m1, n2, m2, color='b', label='same two?')  # 此种对前面的所有曲线生效
print(line1, line2)
plt.legend()  # 使label生效

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


line1, = plt.plot(n, m1, 'r-.p', label='第一条')
# line1 = plt.plot(n, m1, 'r-.p', label='第一条')[0]  和上面的等价，说明plt.plot返回的对象是一个[1,]列表
# 之所以需要一个列表，是因为plt.plot能一次画多个对象
line2, = plt.plot(n, m2)
print(line1, line2)
plt.legend(['first', 'second'])  # 可覆盖原来的，也可只传fisrt，会按顺序apply
plt.legend(handles=[line1, line2], labels=['girl购物欲望','boy购物欲望'], loc='best')  # 可覆盖原来的
plt.show()

# loc参数参见 https://zhuanlan.zhihu.com/p/111108841
# 精确布局(第三种方法)摘录如下
# 当使用loc = (x, y)时，x, y并不是轴域中实际的x, y的值，而是将x轴, y轴分别看成1, 即：
#
# ( x/(x_max-x_min) , y/(y_max-y_min) )（即进行归一化处理）;
#
# 那么，在绘制图表时，若用到坐标轴的范围限制，如xlim=(0, 16), ylim=(0, 9)。在此基础上，如果要将图例放置到点(2, 2)上，loc实际传入的参数应该为：
#
# loc = ( 2/(16-0) , 2/(9-0) )
#
# 即 loc = (2/16, 2/9)
