import numpy as np
import math
import matplotlib as plt
from matplotlib import animation
from matplotlib import patches

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
            print(step)
            points[step] = self.drawer.get_points(step*self.wobble_step, self.drawer.steps)

        return points

    def get_arrow_vals_temporal(self):
        steps = self.get_steps()
        base_points = np.empty([steps, 2])
        vector_vals = np.empty([steps, 2])

        for step in range(0, steps):
            print(step)
            base_points[step] = self.drawer.get_point(0, step*self.wobble_step)
            vector_vals[step] = self.drawer.get_normal(0, step*self.wobble_step)
        
        return (base_points, vector_vals)


    def animate(self, fig, ax):
        points = self.get_cycloid_points_temporal()
        arrow_vals = self.get_arrow_vals_temporal()

        line, = ax.plot([], [], lw = 2)
        angle_per_circle = self.drawer.cycloid.params.pin_count**-1 *2*math.pi

        objects = [line]

        for i in range(0, self.drawer.cycloid.params.pin_count):
            objects.append(plt.patches.Circle((math.cos(angle_per_circle*i), math.sin(angle_per_circle*i)), radius=self.drawer.cycloid.params.pin_r))
            ax.add_artist(objects[-1])
            
        def init():
            line.set_data([], [])
            return objects

        def animate(step):
            this_line = points[step]
            line.set_data(this_line[0], this_line[1])

            arrow_base = arrow_vals[0][step]
            arrow_vec = arrow_vals[1][step]

            arrow = ax.quiver(arrow_base[0], arrow_base[1], arrow_vec[0], arrow_vec[1])

            return np.append(objects, arrow)
        
        return animation.FuncAnimation(fig, animate, init_func=init, blit = True, frames = self.get_steps(), interval=1)