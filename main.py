import matplotlib.pyplot as plt
import sympy as sp
from sympy.abc import W
import sympy.physics.vector as spv
from cycloid import *
from utils import *

tooth_dif = -1
pins = 5
pinwheel_r = 1
pin_r = 0.1
eccentricity = 0.1

c = Cycloid(pins, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle=0, inverted = False)

fig = plt.figure()
ax = plt.axes()

cd = Cycloid_Drawer(c)

ca = Cycloid_Animator(cd)

ani = ca.animate(fig, ax)
plt.axis('equal')

plt.xlim([-2, 2])
plt.ylim([-2, 2])

plt.show()