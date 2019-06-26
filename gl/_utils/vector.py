import numpy as np


def perpendicular_vector(v):
    "A vector that's perpedicular to another 3D vector."
    if v[1] == 0 and v[2] == 0:
        if v[0] == 0:
            return np.array([0., 0., 0.])
        else:
            return np.cross(v, [0., 1., 0.])
    return cross(v, [1., 0., 0.])


def dist(v1, v2):
    'Distance between two points or vectors.'
    return(sum(abs(v1 - v2) ** 2) ** .5)
