import numpy as np
import math
import matplotlib as plt
from matplotlib import animation
from matplotlib import patches
from src.utils.math_utils import *

class Cycloid_Animator:
    def __init__(self, drawer, starting_wobbles = 0, wobble_step = 0.01, ending_wobbles = None):
        self.drawer = drawer
        self.starting_wobbles = starting_wobbles
        self.wobble_step = wobble_step
        if ending_wobbles == None:
            ending_wobbles = abs(starting_wobbles + self.drawer.cycloid.params.get_rot_per_wobble()**-1)
        self.ending_wobbles = ending_wobbles
    
    def get_steps(self):
        return int((self.ending_wobbles - self.starting_wobbles)/self.wobble_step)
    
    def get_cycloid_points_temporal(self):
        steps = self.get_steps()
        points = np.empty([steps, 2, self.drawer.steps])

        for step in range(0, steps):
            points[step] = self.drawer.get_points(step*self.wobble_step, self.drawer.steps)

        return points

    def get_arrow_vals_temporal(self):
        steps = self.get_steps()

        p = self.drawer.cycloid.params

        arrows = np.empty([steps, p.pin_count, 2, 2])

        for step in range(0, steps):
            in_wobbles = step*self.wobble_step
            pin_points = self.drawer.get_pin_pos_arr()

            for n in range(0, p.pin_count):
                wob = self.drawer.cycloid.get_nearest_edge_point_wobs(in_wobbles, self.drawer.get_twist(in_wobbles), pin_points[n], max_depth=10)

            
                arrows[step][n][0] = self.drawer.get_point(wob, step*self.wobble_step)
                arrows[step][n][1] = self.drawer.get_normal(wob, step*self.wobble_step)
        
        return arrows


    def animate(self, fig, ax):
        points = self.get_cycloid_points_temporal()
        arrow_vals_t = self.get_arrow_vals_temporal()

        p = self.drawer.cycloid.params

        line, = ax.plot([], [], lw = 2)

        objects = [line]

        pin_pos_arr = self.drawer.get_pin_pos_arr()

        for pin_pos in pin_pos_arr: 
            objects.append(plt.patches.Circle((pin_pos[0], pin_pos[1]), p.pin_r))
            ax.add_artist(objects[-1])
            
        def init():
            line.set_data([], [])
            return objects

        def animate(step):
            this_line = points[step]
            line.set_data(this_line[0], this_line[1])
            arrow_vals = arrow_vals_t[step]
            arrows = [None] * self.drawer.cycloid.params.pin_count

            for n in range(0, self.drawer.cycloid.params.pin_count):
                arrow_val = arrow_vals[n]
                arrows[n] = ax.quiver(arrow_val[0][0], arrow_val[0][1], arrow_val[1][0], arrow_val[1][1])

            return np.append(objects, arrows)
        
        return animation.FuncAnimation(fig, animate, init_func=init, blit = True, frames = self.get_steps(), interval=1, repeat=False)