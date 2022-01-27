import matplotlib.pyplot as plt
from cycloid_drawer import Cycloid_Drawer
from cycloid_animator import Cycloid_Animator
from cycloid import Cycloid
from cycloid_params import Cycloid_Params

tooth_dif = -1
pins = 5
pinwheel_r = 1
pin_r = 0.1
eccentricity = 0.1



cp = Cycloid_Params(pins, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle=0, inverted = False)

c = Cycloid(cp)

fig = plt.figure()
ax = plt.axes()

cd = Cycloid_Drawer(c)

ca = Cycloid_Animator(cd, wobble_step=0.01)

ani = ca.animate(fig, ax)
plt.axis('equal')

plt.xlim([-2, 2])
plt.ylim([-2, 2])

plt.show()