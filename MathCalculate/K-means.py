# K均值聚类算法
# k均值聚类是使用最大期望算法（Expectation-Maximization algorithm）求解的高斯混合模型（Gaussian Mixture Model, GMM）
# 在正态分布的协方差为单位矩阵，且隐变量的后验分布为一组狄拉克δ函数时所得到的特例

# 思考：为什么按如下算法，一定会收敛而不会陷入无限循环？
# 首先明确一点：对任意一簇点，质心就是这些点坐标计算的平均值，它到这些点的欧式距离的平方和最小。(注意是平方和，用导数很容易证明)
# 故而，得到一个划分后，将原new_center替换此划分的质心，SSE下降(或不变)，重新划分所有的点，由划分过程可知，SSE下降或不变。
# 从kmeans的算法可以发现，SSE其实是一个严格的坐标下降（Coordinate Decendet）过程。
# 由单调有界数列的收敛定理知，一定会收敛。
# 由于SSE是一个非凸函数（non-convex function），所以SSE不能保证找到全局最优解，只能确保局部最优解。
# 但是可以重复执行几次kmeans，选取SSE最小的一次作为最终的聚类结果。

# 另外的评价标准：轮廓系数（Silhouette Coefficient）结合了聚类的凝聚度（Cohesion）和分离度（Separation），用于评估聚类的效果。
# 该值处于-1~1之间，值越大，表示聚类效果越好。
# 轮廓系数的计算公式如下：
# a(i)表示样本i与同一簇中其他样本的平均距离
# 选取x_i外的一个簇B，计算x_i与B中所有点的平均距离，遍历所有其他簇，找到最近的这个平均距离，记作b(i)
# s(i) = (b(i) - a(i)) / max{a(i), b(i)}
# 计算所有样本的轮廓系数的平均值，作为聚类的评价指标

# 优点：
# 1.算法快速、简单;
# 2.对大数据集有较高的效率并且是可伸缩性的;
# 3.时间复杂度近于线性，而且适合挖掘大规模数据集。
#
# 缺点：
# 1.在 K-means 算法中 K 是事先给定的，这个 K 值的选定是非常难以估计的。很多时候，事先并不知道给定的数据集应该分成多少个类别才最合适。
# 2.在 K-means 算法中，首先需要根据初始聚类中心来确定一个初始划分，然后对初始划分进行优化。这个初始聚类中心的选择对聚类结果有较大的影响，一旦初始值选择的不好，可能无法得到有效的聚类结果。
# 3.从 K-means 算法框架可以看出，该算法需要不断地进行样本分类调整，不断地计算调整后的新的聚类中心，因此当数据量非常大时，算法的时间开销是非常大的。

import numpy as np
import pandas as pd
import random
import time


class KMeansClusterer:
    def __init__(self, ndarray, cluster_num):
        self.ndarray = ndarray
        self.cluster_num = cluster_num
        self.points = self.__pick_start_point(ndarray, cluster_num)

    def cluster(self):
        result = []
        for i in range(self.cluster_num):
            result.append([])
        print(self.points)
        for item in self.ndarray:
            distance_min = np.inf  # 从sys.maxsize改为np.inf
            index = -1
            for i in range(len(self.points)):
                distance = self.__distance(item, self.points[i])
                if distance < distance_min:
                    distance_min = distance
                    index = i
            result[index].append(item)
            print("index: ", index, "item: ", item, "result: ", result)
        print("result: ", result)
        # new_center = np.array([])  # 这相当于是生成固定维度的array，在np.append时会有问题
        new_center = None
        for item in result:
            if new_center is None:
                new_center = self.__center(item)
            else:
                # numpy中的append为什么没有类似于Python中的append这样原地操作数据的方法呢？
                new_center = np.append(new_center, self.__center(item), axis=0)
        # 中心点未改变，说明达到稳态，结束递归
        print(self.points, type(self.points))
        print(new_center, type(new_center))
        print(self.points == new_center)
        if (self.points == new_center).all():
            return result

        # 不相等时，更新中心点，继续递归。注意：这里new_center不一定是原点集中的点，它只是原点集某些点集合的质心
        self.points = new_center
        return self.cluster()

    def __center(self, list):
        '''计算一组坐标的中心点
        '''
        # 计算每一列的平均值
        # print(list)
        # print(np.array(list).mean(axis=0))
        # return np.array(list).mean(axis=0)[np.newaxis, :]  # 外面包一层，变成二维
        return np.array(list).mean(axis=0, keepdims=True)  # 直接用keepdims参数

    def __distance(self, p1, p2):
        '''计算两点间距
        '''
        return np.sqrt(np.sum((p1 - p2) ** 2, axis=-1))

    def __pick_start_point(self, ndarray, cluster_num):

        if cluster_num < 0 or cluster_num > ndarray.shape[0]:
            raise Exception("簇数设置有误")

        # 随机点的下标
        indexes = random.sample(np.arange(0, ndarray.shape[0], step=1).tolist(), cluster_num)
        points = []
        for index in indexes:
            points.append(ndarray[index])
        return np.array(points)


if __name__ == '__main__':
    # 每次运行结果不同，说明该算法不稳定，只会收敛到局部最优解
    ndarray = np.arange(1, 11).reshape((-1, 1))
    cluster_num = 3
    k = KMeansClusterer(ndarray, cluster_num)
    print(k.cluster())

    ndarray = np.arange(1, 11).reshape((-1, 2))
    cluster_num = 3
    k = KMeansClusterer(ndarray, cluster_num)
    print(k.cluster())
