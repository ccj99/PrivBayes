import itertools
import operator
import numpy as np
import read_data


def get_N(Dataset, property_matrix, k):
    # TODO property 有可能存在各个属性取值可能长度不同的情况，所以不能用numpy的array
    # 初始化
    dataset_len = Dataset.shape[0]
    property_num = property_matrix.shape[0]
    property_value_range = property_matrix.shape[1]
    N = np.zeros((property_num, property_num), dtype=int)
    V = []
    X_PI_JDs = []
    PI_JDs = []
    # 执行选取第一个无parent的属性，先生成所有属性的集合
    A = []
    i = 7
    for index in range(property_num):
        A.append(index)
    Xi = A[i]
    del A[i]
    N[i] = np.zeros((1, property_num), dtype=int)
    V.append(Xi)
    # 计算在没有parent的情况下的联合分布，也就是Xi 的边缘分布
    joint_distri0 = np.zeros((1, property_num))
    for item in Dataset:
        for index, propertY in enumerate(property_matrix[i]):
            if int(item[i]) == int(propertY):
                joint_distri0[0][index] += 1
    joint_distri0 = joint_distri0 / dataset_len
    X_PI_JDs.append(joint_distri0)



