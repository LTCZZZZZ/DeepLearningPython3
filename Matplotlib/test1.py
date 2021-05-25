import matplotlib.pyplot as plt
import matplotlib

x = [2, 4, 6, 8, 10]
y = [2.1, 3.8, 1.1, 5.6, 6.1]

fig = plt.figure('Figure title 1', figsize=(12, 4))  # 貌似可省略

# 折线样式
# | '-' | '--' | '-.' | ':' | 'None' | ' ' | '' |  后三个是一样的，draw nothing
# 以上样式多用于set_linestyle(ls)函数
plt.plot(x, y, color = 'r', linestyle = '--')  # 折线
# 这个对象如何添加进绘图区？？？？？？？？？？？？？？？？
# l2 = matplotlib.lines.Line2D(x, y)
# l2.set_linestyle('--')
# plt.plot(l2)

# 散点图样式
# . 表示 Point marker o 表示 Circle marker 1 表示 Tripod down marker
# s 表示 Square marker p 表示 Pentagon marker * 表示 Star marker
# + 表示 Plus marker x 表示 Cross (x) marker
plt.scatter(x, y, color='k', marker='o')  # 散点图

# 字体设置，用于显示中文
# print(matplotlib.matplotlib_fname()) # 此目录上级是字体所在目录
# 一般为   .../site-packages/matplotlib/mpl-data/fonts/ttf
# plt.rcParams['font.sans-serif'] = ['SimHei']  # Mac下测试无效，应该还需要更多操作
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac字体册中有此字体
# plt.rcParams['font.sans-serif'] = ['Kai']  # 同样字体册中有此字体却不生效
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号，但目前尚未发现作用
plt.xlabel('时间')
plt.ylabel('温度')

# 标签旋转
plt.xticks(rotation = -30)

plt.show()

# 饼图，与上面两个无法共存
plt.pie(y)
plt.title('PIE')

plt.show()
