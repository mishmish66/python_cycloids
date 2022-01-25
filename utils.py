import numpy as np

def vert(arr):
    return np.vstack(np.array(arr))
    
def get_rot_mat(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])