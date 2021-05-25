import numpy as np


def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    # 下面两式是相等的，但从计算机计算复杂度方面来看，貌似确实是后一个式子计算起来更快，并且感觉还能进一步优化
    # return 1 / (np.exp(z) + 2 + np.exp(-z))
    # return sigmoid(z) * (1 - sigmoid(z))
    s = sigmoid(z)
    return s * (1 - s)  # 感觉在实际计算中，只要知道这个形式就行，这个函数其实用不上


class neuron:

    def __init__(self, w, b, cost='quadratic'):
        # cost为损失函数的类型，目前设三种：'per se'，'quadratic'，'cross-entropy'
        self.w = w
        self.b = b
        # 注意这里cost是损失函数的导函数，下面这一行代码会触发cost.setter，进而返回一个函数（损失函数的导函数）
        self.cost = cost

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        # y是期望输出（为常数），y_是实际输出（为w和b的函数）
        # 注意，下面都用到了sigmoid(z)的导函数是s * (1 - s)
        # 另外，这里都没有带上z对w求导带出的乘数x

        # 直接用(y_ - y)当做损失函数（注意这里隐含y_恒大于y的条件）
        if value == 'per se':
            self._cost = lambda y, y_: y_ * (1 - y_)

        # 一般常用的损失函数，即平方损失函数，这儿就不需要y_ > y的条件了
        elif value == 'quadratic':
            self._cost = lambda y, y_: (y_ - y) * y_ * (1 - y_)

        # 交叉熵函数作为损失函数
        elif value == 'cross-entropy':
            self._cost = lambda y, y_: y_ - y

        # 交叉熵函数作为损失函数（我自己算错了导数后的，但感觉这个形式也不是不能用，就是就图形来看下降过快，有可能会反复震荡）
        else:
            # self._cost = lambda y, y_: (1 - y) / (1 - y_) - y / y_
            self._cost = lambda y, y_: (y_ - y) / ((1 - y_) * y_)
            # 注意观察这个形式，quadratic时是用差乘以一个值，这里是用差除以这个值，
            # 而这个值正是sigmoid(z)的导函数在x处的值

    def __call__(self, x=1, y=0):  # 默认输入值设为1，输出值为0
        self.x = x
        self.y = y
        # 一个有意思的事情是，当x=1时，w和b对函数值的影响是完全相同的，
        # 这意味着，在三维空间中的此曲面z=f(x, y)上任何一点A，
        # 假如距离不是欧式距离，而是定义为d(p, q)=|x(p)-x(q)|+|y(p)-y(q)|的话，
        # 则与A距离相同的点的函数值都相同，即z相等，亦即在同一等高面上
        # 平面z=x + y亦具有此性质
        # 更详细的信息与拓展研究见 sigmoid neuron.ggb 文件
        return sigmoid(self.w * x + self.b)


# n = neuron(0.6, 0.9)
n = neuron(2, 2)
# print(n())
# print(n.cost)  # function

# eta = 0.15
eta = 0.05

i = 0
# n.cost = 'per se'
n.cost = 'cross-entropy'
while True:
    y_ = n()
    y = n.y  # 调用之后才有n.y这个属性
    print(y_)
    if i == 300:
    # if abs(y_ - y) < 0.1:  # 这里理论上来说应该用损失函数来判断？？？但感觉这样判断好像更简洁
        break

    # derivative of the cost function，注意这里是已经求值了
    deriv = n.cost(y, y_)

    delta_w = -eta * deriv * n.x  # 注意这里乘的n.x，是变量z对w求导带出来的，它其实就是输入分量x
    delta_b = -eta * deriv

    n.w += delta_w
    n.b += delta_b
    # print(n.w, n.b)

    i += 1

print(i)
print(n.w, n.b)

