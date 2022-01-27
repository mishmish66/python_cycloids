import sympy as sp
import numpy as np
    
def get_rot_mat(theta):
    c, s = sp.cos(theta), sp.sin(theta)
    return sp.Matrix([[c, -s], [s, c]])

def vert(arr):
    return np.vstack(arr)

def get_np_rot_mat(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])

def vector_magnitude(v):
    mag_sq = v.dot(v)
    return sp.sqrt(mag_sq)

def vector_normalize(v):
    mag = vector_magnitude(v)
    return v * mag**-1

def vector_unwrap(v):
    return [v[0][0], v[1][0]]

def to_np(v):
    return vert(vector_unwrap(v))

def vectors_distance(v1, v2):
    return vector_magnitude(v1 - v2)

def np_mag(v):
    mag_sq = np.dot(np.transpose(v), v)
    return np.sqrt(mag_sq)

def np_vec_dist(v1, v2):
    return np_mag(v1-v2)

