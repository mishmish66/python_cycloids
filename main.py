import matplotlib.pyplot as plt
from sympy import *
import numpy as np
from cycloid import *
from utils import *

tooth_dif = -1
pins = 4
pinwheel_r = 1
pin_r = 0.1
eccentricity = 0.1

c = Cycloid(pins, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle=0)

fig = plt.figure()
ax = plt.axes()

cd = Cycloid_Drawer(c, 256)

ca = Cycloid_Animator(cd, wobble_step=0.01)

ani = ca.animate(fig, ax)

plt.xlim([-2, 2])
plt.ylim([-2, 2])
plt.axis('equal')

plt.show()