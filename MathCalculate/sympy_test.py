from sympy import *

x = Symbol('x', real=True)
y = Symbol('y', real=True)

# 泰勒展开
sin_s = series(sin(x), x, 0, 10)
cos_s = series(cos(x), x, 0, 10)
print('sin(x)={}'.format(sin_s))
print('cos(x)={}'.format(cos_s))

# 求导
print(diff(sin(2 * x), x))
print(diff(x ** 2 + 2 * x + 1, x, 2))
print(diff(x ** 2 * y ** 2 + 2 * x ** 3 + y ** 2, x, 1, y, 1))

# 表达式替换变量或求值
f = x ** 2 + 3 * x + 2
print(f.subs(x, y))
print(f.subs(x, 2))
