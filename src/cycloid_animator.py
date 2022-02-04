from matplotlib.pyplot import axes
import numpy as np
import math
import matplotlib.pyplot as plt
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
            print("getting edge vals step " + str(step) + "/" + str(steps))
            points[step] = self.drawer.get_points(step*self.wobble_step, self.drawer.steps)

        return points

    def get_arrow_vals_temporal(self):
        steps = self.get_steps()

        p = self.drawer.cycloid.params

        arrows = np.zeros([steps, p.pin_count, 2, 2])
        wasted_forces = np.zeros(steps)

        for step in range(0, steps):
            print("getting arrow vals step " + str(step) + "/" + str(steps))
            c = self.drawer.cycloid

            in_wobbles = step*self.wobble_step
            pin_points = self.drawer.get_pin_pos_arr()

            point_norms = np.zeros([p.pin_count, 2, 2])

            center = c.get_wobble_center(in_wobbles)

            twist = c.get_twist(in_wobbles)

            vel = c.get_vel_from_wobbles(in_wobbles, center)

            for n in range(0, p.pin_count):
                point_draw_wob = c.get_nearest_edge_point_wobs(in_wobbles, twist, pin_points[n], max_depth=10)

                point = self.drawer.get_point(point_draw_wob, in_wobbles)
                norm = c.get_outward_normal(point_draw_wob, twist, center, vert(point))

                point_norms[n][0] = hor(point)
                point_norms[n][1] = hor(norm)

            arrows[step] = c.resolve_forces(point_norms, in_wobbles, center)

            step_arrows = arrows[step]

            step_mags = np.fromiter((np_mag(arrow[1]) for arrow in step_arrows), dtype=step_arrows.dtype)
            step_wasted = np.fromiter((np.dot(hor(np_normalize(vert(arrow[0]))), arrow[1]) for arrow in step_arrows), dtype=step_arrows.dtype)
            step_waste = np.sum(step_wasted)
            step_force = np.sum(step_mags)
            wasted_forces[step] = step_waste/step_force

        
        return (arrows, np.average(wasted_forces))


    def animate(self, fig, ax):
        points = self.get_cycloid_points_temporal()
        arrow_vals_t, waste = self.get_arrow_vals_temporal()
        print("WASTED FORCE: " + str(waste))
        steps = self.get_steps()

        p = self.drawer.cycloid.params

        line, = ax.plot([], [], lw = 2)

        objects = [line]

        pin_pos_arr = self.drawer.get_pin_pos_arr()

        for pin_pos in pin_pos_arr:
            objects.append(patches.Circle((pin_pos[0], pin_pos[1]), p.pin_r))
            ax.add_artist(objects[-1])
            
        def init():
            line.set_data([], [])
            objects.append(plt.text(-0.25, -1.25, "Wasted Force: " + str(waste)))
            return objects

        def animate(step):
            this_line = points[step]
            line.set_data(this_line[0], this_line[1])
            arrow_vals = arrow_vals_t[step]

            arrows = np.array([])

            for n in range(0, p.pin_count):
                arrows = np.append(arrows, ax.quiver(arrow_vals[n][0][0], arrow_vals[n][0][1], arrow_vals[n][1][0], arrow_vals[n][1][1], scale = 1, scale_units = 'xy', width = 0.005))

            print("frame: " + str(step) + "/" + str(steps))
            return np.append(objects, arrows)
        
        return animation.FuncAnimation(fig, animate, init_func=init, blit = True, frames = self.get_steps(), interval=1, repeat=False)