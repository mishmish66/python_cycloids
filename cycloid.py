from enum import auto
from locale import normalize
from multiprocessing.connection import wait
from tkinter.ttk import setup_master
from utils import *
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import sympy as sp
import numpy as np
sym_wobbles = sp.symbols('wob')
from sympy.utilities.autowrap import autowrap

class Cycloid:
    def __init__(self, pin_count, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle, inverted):
        self.pin_count = pin_count
        self.tooth_dif = tooth_dif
        self.pinwheel_r = pinwheel_r
        self.pin_r = pin_r
        self.eccentricity = eccentricity
        self.offset_angle = offset_angle
        self.inverted = inverted

        draw_wobbles, input_wobbles, twist = sp.symbols('dw iw tw')

        expr = self.sym_get_point_from_wobbles(draw_wobbles, input_wobbles, twist)

        self.get_point_from_wobbles = autowrap(expr, args=[ draw_wobbles, input_wobbles, twist ])

        expr = self.sym_get_normal_from_wobbles(draw_wobbles, input_wobbles, twist)

        self.get_normal_from_wobbles = autowrap(expr, args=[ draw_wobbles, input_wobbles, twist ])

    def sym_get_wobble_center(self, input_wobbles):
        return sp.MatMul(get_rot_mat(input_wobbles*2*sp.pi), sp.Matrix([self.eccentricity, 0]))
    
    def get_wobble_center(self, input_wobbles):
        return np.matmul(get_np_rot_mat(input_wobbles*2*np.pi), vert([self.eccentricity, 0]))

    def sym_get_point_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        center_pos = self.sym_get_wobble_center(input_wobbles)
        wobble_pos = sp.MatMul(get_rot_mat(draw_wobbles*2*sp.pi + self.offset_angle + twist), sp.Matrix([-self.eccentricity, 0]))
        rotation_pos = sp.MatMul(get_rot_mat(draw_wobbles*2*sp.pi * self.draw_rot_per_wobble() + self.offset_angle + twist), sp.Matrix([self.pinwheel_r, 0]))
        return center_pos + wobble_pos + rotation_pos
    
    def sym_get_edge_point_from_wobbles(self, draw_wobbles, input_wobbles, twist, normal = None):
        center = self.sym_get_wobble_center(input_wobbles)
        point = self.sym_get_point_from_wobbles(draw_wobbles, input_wobbles, twist)

        v1 = point + normal * self.pin_r
        v1 = sp.simplify(v1)

        v2 = point - normal * self.pin_r
        v2 = sp.simplify(v2)

        d1 = vectors_distance(v1, center)
        d2 = vectors_distance(v2, center)

        return sp.Piecewise((v1, d1 > d2), (v2, True))
    
    def get_edge_point_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        center_pos = to_np(self.get_wobble_center(input_wobbles))
        point = to_np(self.get_point_from_wobbles(draw_wobbles, input_wobbles, twist))
        normal = to_np(self.get_normal_from_wobbles(draw_wobbles, input_wobbles, twist))

        p1 = point + normal * self.pin_r
        p2 = point - normal * self.pin_r

        cond = np_vec_dist(p1, center_pos) < np_vec_dist(p2, center_pos)
        
        if self.inverted:
            cond = not cond

        if cond:
            return p1
        else:
            return p2


    def sym_get_normal_from_wobbles(self, draw_wobbles, input_wobbles, twist):

        point = self.sym_get_point_from_wobbles(draw_wobbles, input_wobbles, twist)

        point = sp.simplify(point)

        vel = sp.diff(point, draw_wobbles)

        tan = vector_normalize(vel)

        tan = sp.simplify(tan)

        curv = sp.diff(tan, draw_wobbles)

        norm = vector_normalize(curv)

        expr = sp.simplify(norm)

        return expr


    def draw_rot_per_wobble(self):
        return -self.tooth_dif/self.pin_count
    
    def get_rot_per_wobble(self):
        return -self.tooth_dif/(self.pin_count + self.tooth_dif)

class Cycloid_Drawer:
    def __init__(self, cycloid, steps = 1024):
        self.steps = steps
        self.cycloid = cycloid
            
    def plot_cycloid(self, ax, input_wobbles = 0,  steps = 1024):
        points = self.get_points(input_wobbles, steps)
        ax.plot(points[0], points[1])

    def get_twists(self, input_wobbles):
        return self.cycloid.offset_angle - input_wobbles*self.cycloid.get_rot_per_wobble()*2*math.pi

    def get_point(self, draw_wobbles = 0, input_wobbles = 0, twists = None):
        if twists == None:
            twists = self.get_twists(input_wobbles)
        vec = self.cycloid.get_edge_point_from_wobbles(draw_wobbles, input_wobbles, twists)

        return vector_unwrap(vec)
            
    def get_points(self, input_wobbles = 0, steps = 1024, twists = None):
        if twists == None:
            twists = self.get_twists(input_wobbles)
        points_x = np.empty(int(steps))
        points_y = np.empty(int(steps))

        wobbles = self.cycloid.draw_rot_per_wobble()**-1
        wobbles_per_step = wobbles/steps

        for i in range(0, steps):
            point = self.get_point(wobbles_per_step*i, input_wobbles, twists)
            points_x[i] = point[0]
            points_y[i] = point[1]
    
        return [points_x, points_y]
        
    def get_normal(self, draw_wobbles = 0, input_wobbles = 0, twist = None):
        try:
            vec = self.cycloid.get_normal_from_wobbles(draw_wobbles, input_wobbles, twist)
        except:
            vec = self.cycloid.get_normal_from_wobbles(draw_wobbles, input_wobbles, self.get_twists(input_wobbles))

        return vector_unwrap(vec)

class Cycloid_Animator:
    def __init__(self, drawer, starting_wobbles = 0, wobble_step = 0.01, ending_wobbles = None):
        self.drawer = drawer
        self.starting_wobbles = starting_wobbles
        self.wobble_step = wobble_step
        if ending_wobbles == None:
            ending_wobbles = abs(starting_wobbles + self.drawer.cycloid.get_rot_per_wobble()**-1)
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
        base_points = np.empty([steps, 2])
        vector_vals = np.empty([steps, 2])

        for step in range(0, steps):
            base_points[step] = self.drawer.get_point(0, step*self.wobble_step)
            vector_vals[step] = self.drawer.get_normal(0, step*self.wobble_step)
        
        return (base_points, vector_vals)


    def animate(self, fig, ax):
        points = self.get_cycloid_points_temporal()
        arrow_vals = self.get_arrow_vals_temporal()

        line, = ax.plot([], [], lw = 2)
        angle_per_circle = self.drawer.cycloid.pin_count**-1 *2*math.pi

        objects = [line]

        for i in range(0, self.drawer.cycloid.pin_count):
            objects.append(plt.Circle((math.cos(angle_per_circle*i), math.sin(angle_per_circle*i)), radius=self.drawer.cycloid.pin_r))
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