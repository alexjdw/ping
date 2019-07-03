import numpy as np

def translate_matrix(mtrx, x, y, z):
    m = np.identity(4)
    m[0][3] = x
    m[1][3] = y
    m[2][3] = z

def rotate_matrix(mtrx, angle, x, y, z):
    pass

def scale_matrix(mtrx, x, y, z):
    m = np.identity(4)
    m[0][0] = x
    m[1][1] = y
    m[2][2] = z
    return m
