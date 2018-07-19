from nltk import flatten
from openpyxl import Workbook
from numpy import *
import itertools
import operator
import numpy as np

filename = '/Users/jerry/Downloads/高维多属性数据集/nltcs.dat'
properties = [[]]


def get_dataset():
    Dataset = np.zeros((1000, 10))
    for i in range(1000):
        for j in range(10):
            Dataset[i][j] = int(random.random() * 3)
    return Dataset


def get_nltcs():
    file = open(filename)
    Dataset = []
    npData = np.zeros((21575, 16), dtype=int)
    for line in file.readlines():
        if line == "21574\n":
            continue
        line_list = line[0:31].split('\t')
        Dataset.append(line_list)
        # print(line_list)
    for i, item in enumerate(Dataset):
        for j, valu in enumerate(item):
            npData[i][j] = int(valu)
            # print(npData[i][j], end=' ')
        # print()
    return Dataset


def get_properties():
    properties = np.zeros((16, 2))
    for i in range(16):
        for j in range(2):
            properties[i][j] = int(j)
    return properties


def get_mutual_information(Dataset, properities, pair, txt_to):
    sumI = 0
    X = properities[pair[0]]
    PI = properities[pair[1][0]]
    for j in range(1, len(pair[1])):
        PI = itertools.product(PI, properities[j])
    PI = list(itertools.chain.from_iterable([PI,]))
    # print(type(PI), PI)
    joint_dirtrib = np.zeros((len(X), len(PI)))
    pi_distrib = np.zeros((1, len(PI)))
    for index_x, x in enumerate(X):
        for index_pi, pi in enumerate(PI):
            unitSum = 0
            xSum = 0
            piSum = 0
            allSum = 0
            mutualInfo = 0
            if str(type(pi)) == "<class 'numpy.float64'>":
                pi = [pi,]
            else: pi = list(pi)
            for item in Dataset:
                allSum += 1
                valueOfData = []
                for j in pair[1]:
                    valueOfData.append(int(item[j]))
                pi = flatten(pi)
                if int(item[pair[0]]) == int(x) and operator.eq(pi, valueOfData):
                    unitSum += 1
                if int(item[pair[0]]) == int(x):
                    xSum += 1
                if operator.eq(pi, valueOfData):
                    piSum += 1
            # if xSum == 0:
            # print(unitSum, xSum, piSum, allSum)
            unitDistrib = unitSum / allSum
            xDistrib = xSum / allSum
            piDistrib = piSum / allSum
            joint_dirtrib[index_x][index_pi] = unitDistrib
            pi_distrib[0][index_pi] = piDistrib
            # txt_to.write('联合分布：' + str(unitDistrib) + ' x的边缘分布：'+ str(xDistrib) + ' pi的边缘分布：'+ str(piDistrib) + '\n')
            # print('联合分布：' + str(unitDistrib) + ' x的边缘分布：'+ str(xDistrib) + ' pi的边缘分布：'+ str(piDistrib) + '\n')
            if xDistrib == 0 or piDistrib == 0:
                mutualInfo = 0
                # print('0')
            else: mutualInfo += unitDistrib * log2(unitDistrib / (xDistrib * piDistrib))
            # print(mutualInfo, type(mutualInfo))
            if isnan(mutualInfo) :
                # print(mutualInfo)
                # print(unitSum, xSum, piSum, allSum)
                mutualInfo = 0
            sumI += mutualInfo
    # print('sum' , sumI)
    return sumI, joint_dirtrib, pi_distrib


def get_n(Dataset, properties, k):
    txt_to = open('/Users/jerry/PycharmProjects/PrivBayes/k=3.txt', 'w')
    N = np.zeros((16,16), dtype=int)
    V = []
    X_PI_JDs = []
    PI_JDs = []
    A = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    i = 7
    Xi = A[i]
    del A[i]
    N[i] = np.zeros((1, 16), dtype=int)
    V.append(Xi)
    # print(len(properties[0]))
    JD0 = np.zeros((1, len(properties[0])))
    allSum = 0
    for item in Dataset:
        for index, property in enumerate(properties[0]):
            if int(item[0]) == int(property):
                JD0[0][index] += 1
            allSum += 1
    JD0 = JD0 / allSum
    X_PI_JDs.append(JD0)
    PI_JDs.append([])
    for i in range(len(A)):
        omega = []
        # for a in A:
        #     for j in range(1,k + 1):
        #         for l in itertools.combinations(V,j):
        #             omega.append([a, l])
        for j in range(1, k + 1):
            for l in itertools.combinations(V, j):
                for a in A:
                    omega.append([a, l])
        Imax = 0
        ImaxPair = []
        Imax_J_D = []
        Imax_P_D = []
        for pair in omega:
            (I, joint_distrib, pi_distrib) = get_mutual_information(Dataset, properties, pair, txt_to)
            # txt_to.write('此AP对为：'+ str(pair) + ' 互信息为：'+ str(I) + '\n')
            print('此AP对为：'+ str(pair) + ' 互信息为：'+ str(I))
            if I > Imax:
                Imax = I
                ImaxPair = pair
                Imax_J_D = joint_distrib
                Imax_P_D = pi_distrib
        # txt_to.write('最大互信息为：'+ str(Imax)+ ' 最大互信息对应的AP对为：'+ str(ImaxPair) + '\n')
        print('最大互信息为：'+ str(Imax)+ ' 最大互信息对应的AP对为：'+ str(ImaxPair))
        for column in ImaxPair[1]:
            N[ImaxPair[0]][column] = 1
        V.append(ImaxPair[0])
        X_PI_JDs.append(Imax_J_D)
        PI_JDs.append(Imax_P_D)
        A.remove(ImaxPair[0])
    txt_to.close()
    return N, X_PI_JDs, PI_JDs


def main():
    wb = Workbook()
    wb.create_sheet('')
    # Dataset = get_dataset()
    Dataset = get_nltcs()
    properties = get_properties()
    # get_mutual_information(Dataset, properties, [0, (7, 6, 8)])
    N, joint_distrib, pi_distrib = get_n(Dataset, properties, 2)
    for i in range(16):
        for j in range(16):
            print(N[i][j], end=' ')
        print()
    return N, joint_distrib, pi_distrib


if __name__ == '__main__':
    main()
    # get_nltcs()