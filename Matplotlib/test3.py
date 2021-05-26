import matplotlib.pyplot as plt

# 这里建立的画布大小是5*5的，并不是坐标轴范围，使用“十字按钮”拖动你就懂了！
plt.figure(figsize=(5, 5))
plt.plot()  # 画个只有坐标系的图（因为没有传参数，所以显示空白）
# plt.show()

ax = plt.gca()

# 下面两行代码貌似可以省略
# 获取你想要挪动的坐标轴，这里只有顶部、底部、左、右四个方向参数
# ax.xaxis.set_ticks_position('bottom')  # 要挪动底部的X轴，所以先目光锁定底部！
# ax.yaxis.set_ticks_position('left')

# 在这里，position位置参数有三种，这里用到了“按Y轴刻度位置挪动”
# 'data'表示按数值挪动，其后数字代表挪动到Y轴的刻度值
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data',0))

ax.spines['top'].set_color('none')  # 设置顶部支柱的颜色为空
ax.spines['right'].set_color('none')  # 设置右边支柱的颜色为空

# 标签会在轴上，很丑
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.xlabel('X轴')
plt.ylabel('Y轴')

plt.show()
