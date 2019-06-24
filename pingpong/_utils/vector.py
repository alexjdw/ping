from numpy import cross

def perpendicular_vector(v):
    if v[1] == 0 and v[2] == 0:
        if v[0] == 0:
            return np.array([0., 0., 0.])
        else:
            return np.cross(v, [0., 1., 0.])
    return cross(v, [1., 0., 0.])