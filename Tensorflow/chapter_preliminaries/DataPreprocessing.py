import os
import pandas as pd
import tensorflow as tf

# os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

# 初始数据
# os.makedirs(os.path.join('..', 'data'), exist_ok=True)  # 递归创建目录
data_file = os.path.join('..', 'data', 'house_tiny.csv')
with open(data_file, 'w') as f:
    f.write('NumRooms,Alley,SelfDefine,Price\n')  # 列名
    f.write('NA,Pave,A,127500\n')  # 每行表示一个数据样本
    f.write('2,NA,B,106000\n')
    f.write('4,NA,,178100\n')
    f.write('NA,NA,,140000\n')


# 处理数据
data = pd.read_csv(data_file)
print(data)

inputs, outputs = data.iloc[:, 0:3], data.iloc[:, 3]
inputs = inputs.fillna(inputs.mean())
print(inputs)

inputs = pd.get_dummies(inputs, columns=['Alley', 'SelfDefine'], dummy_na=True)  # 注意columns必须传一个list-like对象
print(inputs)

# 转换为张量格式
print(type(inputs.values))  # <class 'numpy.ndarray'>
X, y = tf.constant(inputs.values), tf.constant(outputs.values)
print(X)
print(y)
