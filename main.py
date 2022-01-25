import matplotlib.pyplot as plt
from sympy import *
import numpy as np
from cycloid import *
from utils import *

steps = 1024

tooth_dif = -1
pins = 5
pinwheel_r = 1
pin_r = 0.1
eccentricity = 0.1

rm = get_rot_mat(0)

vec = np.vstack([1, 0])

mult = np.matmul(rm, vec)

c = Cycloid(pins, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle=0)

wobble_per_step = (c.get_rot_per_wobble())**-1/steps

points_x = np.empty([steps])
points_y = np.empty([steps])

for i in range(0, steps):
    point = c.get_point_from_wobbles(wobble_per_step*i, 0)

    points_x[i] = point[0]
    points_y[i] = point[1]

fig, ax = plt.subplots(figsize=(2,2), constrained_layout=True)
ax.plot(points_x, points_y)
plt.axis('equal')
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.show()