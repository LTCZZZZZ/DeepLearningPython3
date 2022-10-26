# 梯度场Gradient Field
import numpy as np
import matplotlib.pyplot as plt


def f(x, y):
    return x ** 2 - y ** 2


def grad_x(f, x, y):
    h = 1e-4
    return (f(x + h / 2, y) - f(x - h / 2, y)) / h


def grad_y(f, x, y):
    h = 1e-4
    return (f(x, y + h / 2) - f(x, y - h / 2)) / h


def numerical_gradient(f, P):
    grad = np.zeros_like(P)
    for i in range(P[0].size):
        grad[0][i] = grad_x(f, P[0][i], P[1][i])
        grad[1][i] = grad_y(f, P[0][i], P[1][i])
    return grad


x = np.arange(-2, 2, 0.25)
y = np.arange(-2, 2, 0.25)

X, Y = np.meshgrid(x, y)
X = X.flatten()
Y = Y.flatten()

grad = numerical_gradient(f, np.array([X, Y]))

plt.quiver(X, Y, grad[0], grad[1])  # grad[0]是一个1*X.size的数组
plt.xlim([-2, 2])
plt.ylim([-2, 2])
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.show()
