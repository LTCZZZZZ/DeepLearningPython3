# 参考及代码来源 https://tensorflow.google.cn/guide/function
import traceback
import contextlib
import tensorflow as tf

# tf.config.run_functions_eagerly(True) # globally disable tf.function


# Some helper code to demonstrate the kinds of errors you might encounter.
@contextlib.contextmanager
def assert_raises(error_class):
    try:
        yield
    except error_class as e:
        print('Caught expected exception \n  {}:'.format(error_class))
        traceback.print_exc(limit=2)  # limit参数指定追踪栈的深度
    except Exception as e:
        raise e
    else:
        raise Exception('Expected {} to be raised but no error was raised!'.format(
            error_class))


@tf.function
def double(a):
    print("Tracing with", a)
    return a + a


print(double(tf.constant(1)))
print()
print(double.pretty_printed_concrete_signatures())
print(double(tf.constant(1.1)))
print()
print(double(tf.constant("a")))
print()
print(double(tf.constant(2.2)))  # 此次前面有编译后的缓存，故不会再编译
print()
print(double.pretty_printed_concrete_signatures())  # 可以看出，内存中缓存了所有不同的编译结果


# shape=[None]表示有一个维度，但这个维度不指定长度；如果想不指定维数，可以使用shape=None
@tf.function(input_signature=(tf.TensorSpec(shape=[None], dtype=tf.int32),))
def next_collatz(x):
    print("Tracing with", x)
    return tf.where(x % 2 == 0, x // 2, 3 * x + 1)


print(next_collatz(tf.constant([1, 2])))
print(next_collatz(tf.constant([1, 2, 3])))  # 如果是shape=[2]，此行会报错
# You specified a 1-D tensor in the input signature, so this should fail.
with assert_raises(ValueError):
    next_collatz(tf.constant([[1, 2], [3, 4]]))

# You specified an int32 dtype in the input signature, so this should fail.
with assert_raises(ValueError):
    next_collatz(tf.constant([1.0, 2.0]))

# 从原函数生成的concrete function，有些类似于python原生的偏函数，但更像一般静态语言的"泛型"的固化
# 这个过程中如果函数有多个参数，可以指定其中一部分为定值(可为python原生对象int等)，妥妥的偏函数
double_strings = double.get_concrete_function(tf.TensorSpec(shape=[], dtype=tf.string))
print(double_strings)
print(double_strings(tf.constant("sky")))

# Obtaining graphs（获得计算图）
for node in double_strings.graph.as_graph_def().node:
    print(f'{node.input} -> {node.name}')

# inspect the code autograph generates （查看自动计算图生成的代码）
print(tf.autograph.to_code(double.python_function))
