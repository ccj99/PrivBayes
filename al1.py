import numpy as np
import random
import math
import al2


def sign(x):
    if x >= 0: return 1
    return -1


def uniform(x):
    return x + random.random()


def get_lap_noise(lamBda):
    u = uniform(-0.5)
    return - lamBda * sign(u) * math.log2(1 - 2 * abs(u))


def main():
    P = []
    Q = []
    k = 2
    d = 10
    epsilon = math.log1p(3)
    n = 1000
    lamBda = 4 * (d - k) / (n * epsilon)
    N, joint_distribs, pi_distribs = al2.main()
    Prk1 = []
    for index in range(k, d):
        sum_pr = 0
        joint_distrib = joint_distribs[index]
        pi_distrib = pi_distribs[index]
        for i in range(joint_distrib.shape[0]):
            for j in range(joint_distrib.shape[1]):
                tmp = joint_distrib[i][j] + get_lap_noise(lamBda)
                if tmp < 0: joint_distrib[i][j] = 0
                else: joint_distrib[i][j] = tmp
                sum_pr += joint_distrib[i][j]
        joint_distrib = joint_distrib / sum_pr
        # print(k, 'i = ', index)
        if index == k :
            Prk1 = joint_distrib
        for i in range(joint_distrib.shape[0]):
            for j in range(joint_distrib.shape[1]):
                joint_distrib[i][j] = joint_distrib[i][j] / pi_distrib[0][j]
        P.append(joint_distrib)
    # print(Prk1)
    for i in range(k):
        # print('k:', k)
        conditional_distrib = Prk1
        Q.append(conditional_distrib)
    # for item in Q:
    #     print(item)
    Q.extend(P)
    P = Q
    for item in P:
        print(item)



if __name__ == '__main__':
    main()