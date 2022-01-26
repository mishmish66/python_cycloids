import sympy as sp
    
def get_rot_mat(theta):
    c, s = sp.cos(theta), sp.sin(theta)
    return sp.Matrix([[c, -s], [s, c]])

def vector_magnitude(v):
    mag_sq = v.dot(v)
    return sp.sqrt(mag_sq)

def vector_normalize(v):
    mag = vector_magnitude(v)
    return v * mag**-1

def vector_unwrap(v):
    return [v[0][0], v[1][0]]