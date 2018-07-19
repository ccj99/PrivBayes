import itertools
import numpy as np
from numpy import *
import al2
import numpy
import operator


def get_propertity():
    property = np.zeros((16, 2))
    for i in range(16):
        for j in range(2):
            property[i][j] = int(j)
    return property

def main():
    Dataset = al2.get_nltcs()
    properties = get_propertity()
    all_sum = 0
    attr_sum = np.zeros((2, 2))
    margin_sum = np.zeros((1, 4))
    joint_sum = np.zeros((2, 8))
    for item in Dataset:
        all_sum += 1
        if int(item[5]) == 1:
            attr_sum[0][0] += 1
            if int(item[7]) == 1 and int(item[6]) == 1:
                margin_sum[0][0] += 1
                joint_sum[0][0] += 1
            elif int(item[7]) == 1 and int(item[6]) == 0:
                margin_sum[0][1] += 1
                joint_sum[0][1] += 1
            elif int(item[7]) == 0 and int(item[6]) == 1:
                margin_sum[0][2] += 1
                joint_sum[0][2] += 1
            else:
                margin_sum[0][3] += 1
                joint_sum[0][3] += 1
        else:
            attr_sum[0][1] += 1
            if int(item[7]) == 1 and int(item[6]) == 1:
                margin_sum[0][0] += 1
                joint_sum[0][4] += 1
            elif int(item[7]) == 1 and int(item[6]) == 0:
                margin_sum[0][1] += 1
                joint_sum[0][5] += 1
            elif int(item[7]) == 0 and int(item[6]) == 1:
                margin_sum[0][2] += 1
                joint_sum[0][6] += 1
            else:
                margin_sum[0][3] += 1
                joint_sum[0][7] += 1
        if int(item[8]) == 1:
            attr_sum[1][0] += 1
            if int(item[7]) == 1 and int(item[6]) == 1:
                joint_sum[1][0] += 1
            elif int(item[7]) == 1 and int(item[6]) == 0:
                joint_sum[1][1] += 1
            elif int(item[7]) == 0 and int(item[6]) == 1:
                joint_sum[1][2] += 1
            else:
                joint_sum[1][3] += 1
        else:
            attr_sum[1][1] += 1
            if int(item[7]) == 1 and int(item[6]) == 1:
                joint_sum[1][4] += 1
            elif int(item[7]) == 1 and int(item[6]) == 0:
                joint_sum[1][5] += 1
            elif int(item[7]) == 0 and int(item[6]) == 1:
                joint_sum[1][6] += 1
            else:
                joint_sum[1][7] += 1
    print(all_sum)
    print('5 和 8 的边缘分布：', attr_sum)
    print('(7 , 6)对的边缘分布：', margin_sum)
    print('(5, 7, 6)联合分布：', joint_sum[0])
    print('(8, 7, 6)联合分布：', joint_sum[1])
    attr_sum = attr_sum / all_sum
    margin_sum = margin_sum / all_sum
    joint_sum = joint_sum / all_sum
    I1 = 0
    I2 = 0
    for i in range(8):
        I1 += joint_sum[0][i] * log2(joint_sum[0][i]/ (attr_sum[0][int(i/4)] * margin_sum[0][i % 4]))
        I2 += joint_sum[1][i] * log2(joint_sum[1][i]/ (attr_sum[1][int(i/4)] * margin_sum[0][i % 4]))
    print('[5, (7, 6)]的互信息为：', I1)
    print('[8, (7, 6)]的互信息为：', I2)
    # print(all_sum, attr_sum, unit_sum00, unit_sum01, unit_sum10, unit_sum11)
    # attr_propability = attr_sum / all_sum
    # unit_propabality11 = unit_sum11 / all_sum
    # unit_propabality10 = unit_sum10 / all_sum
    # unit_propabality01 = unit_sum01 / all_sum
    # unit_propabality00 = unit_sum00 / all_sum
    # Imax = 0
    # for i in range(16):
    #     if i != 7:
    #         I = unit_propabality11[0][i]*log2(unit_propabality11[0][i]/(attr_propability[0][i] * attr_propability[0][7]))\
    #           + unit_propabality10[0][i]*log2(unit_propabality10[0][i]/(attr_propability[0][i] * (1 - attr_propability[0][7])))\
    #           + unit_propabality01[0][i]*log2(unit_propabality01[0][i]/((1 - attr_propability[0][i]) * attr_propability[0][7]))\
    #           + unit_propabality00[0][i]*log2(unit_propabality00[0][i]/((1 - attr_propability[0][i]) * (1 - attr_propability[0][7])))
    #         # print(I)
    #         if I > Imax:
    #             Imax = I
    #             print(i + 1)



if __name__ == '__main__':
    main()
    # a = [1.0, 1.0, 1.0]
    # A = [1, 1, 1]
    # print(operator.eq(a, A))