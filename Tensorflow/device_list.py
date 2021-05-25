# 另参见 https://stackoverflow.com/questions/52943489/what-is-xla-gpu-and-xla-cpu-for-tensorflow

# import tensorflow as tf
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())
