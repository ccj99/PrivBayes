import numpy as np


filename = '/Users/jerry/Downloads/高维多属性数据集/nltcs.dat'


def read_file(filename):
    file = open(filename)
    Dataset = []
    attr_num = 16
    first_line = '21574'
    for line in file.readlines():
        if line == first_line + "\n":
            continue
        line_list = line[0:attr_num * 2 - 1].split('\t')
        Dataset.append(line_list)
        # print(line_list)
    length = len(Dataset)
    npData = np.zeros((length, attr_num), dtype=int)
    for i, item in enumerate(Dataset):
        for j, valu in enumerate(item):
            npData[i][j] = int(valu)
            print(npData[i][j], end=' ')
        print()
    return Dataset, length


def get_property():
    bias = 0
    value_range = 2
    attr_num = 16
    property_matrix = np.zeros((attr_num, value_range), dtype=int)
    for i in range(attr_num):
        for j in range(value_range):
            property_matrix[i][j] = int(j)
    return property_matrix




if __name__ == '__main__':
    get_property()