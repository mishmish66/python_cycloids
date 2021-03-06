import matplotlib.pyplot as plt
from src.cycloid_drawer import Cycloid_Drawer
from src.cycloid_animator import Cycloid_Animator
from src.double_cycloid_animator import Double_Cycloid_Animator
from src.cycloid import Cycloid
from src.cycloid_params import Cycloid_Params
from matplotlib import animation
import numpy as np

scale = 0.01

tooth_dif_1 = 1
pins_1 = 7
pinwheel_r_1 = 70*scale
pin_r_1 = 7*scale

tooth_dif_2 = 1
pins_2 = 10
pinwheel_r_2 = 27*scale
pin_r_2 = 7*scale
eccentricity = 2*scale
save = False

cp1 = Cycloid_Params(pins_1, tooth_dif_1, pinwheel_r_1, pin_r_1,
                    eccentricity, offset_angle=0, internal=False)

cp2 = Cycloid_Params(pins_2, tooth_dif_2, pinwheel_r_2, pin_r_2,
                    eccentricity, offset_angle=0, internal=True)

c1 = Cycloid(cp1)
c2 = Cycloid(cp2)

fig = plt.figure()
ax = plt.axes()

cd1 = Cycloid_Drawer(c1)
cd2 = Cycloid_Drawer(c2)

ca = Double_Cycloid_Animator(cd1, cd2, wobble_step=0.01)
#ca = Cycloid_Animator(cd1, wobble_step=0.01)

ani = ca.animate(fig, ax)


plt.axis('equal')
plt.xlim([-2, 2])
plt.ylim([-2, 2])

if save:
    ani.save("cycloid.mp4", fps=60)

plt.show()
