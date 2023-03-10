import gzip
import pickle
import numpy as np

f = gzip.open('mnist.pkl.gz', 'rb')
training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
f.close()

print(len(training_data))
print(training_data[0].shape)
print(training_data[1].shape)
print(training_data[1][:10])
# print(test_data[0].shape)

class Network:

    def __init__(self, size):
        pass

    def __call__(self, *args, **kwargs):
        pass


# w1 = np.zeros((784, 30))
w1 = np.random.randn(784, 30)
b1 = np.zeros((30,))
w2 = np.random.randn(30, 10)
b2 = np.zeros((10,))

y_hat = np.dot((np.dot(training_data[0], w1) + b1), w2) + b2

net = Network([784, 30, 10])
print(y_hat[0])



def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))
