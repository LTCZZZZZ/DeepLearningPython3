# 参见 https://zhuanlan.zhihu.com/p/111810019

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(12, 4))  # 不管是否填充子图区域，一次性将所有子图Axes构建完成

ax1 = axes[0, 1]  # 从左到右从上到下，按照矩阵形式去对应位置
ax1.plot(pd.Series(np.random.randn(1000).cumsum()))

ax2 = axes[1, 2]
ax2.plot(pd.DataFrame(np.random.randn(30, 2), columns=['A', 'B']))

ax3 = axes[1, 0]
data = pd.DataFrame(np.random.randn(30, 2), columns=['A', 'B'])
ax3.scatter(data['A'], data['B'])

fig2 = plt.figure(num=2, figsize=(5, 3))
fig2_ax1 = fig2.add_subplot(111)
fig2_ax1.plot(np.random.rand(40).cumsum(), 'r--')

# fig.show(0)
plt.show()
