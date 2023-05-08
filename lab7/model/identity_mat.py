import numpy


def identity_mat44():  # возвращает единичную матрицу 4x4
    return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')
