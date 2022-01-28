from os import path
import numpy as np
from sympy import parallel_poly_from_expr
from src.utils.func_utils import get_funcs
from src.utils.math_utils import (np_mag, to_np, np_vec_dist, get_np_rot_mat, vert)

class Cycloid:
    def __init__(self, cycloid_params):
        self.params = cycloid_params
        self.imported_funcs = get_funcs()
    
    def get_wobble_center(self, input_wobbles):
        return np.matmul(get_np_rot_mat(input_wobbles*2*np.pi), vert([self.params.eccentricity, 0]))
    
    def get_point_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        p = self.params
        return self.imported_funcs["get_point_from_wobbles"](draw_wobbles, p.eccentricity, input_wobbles, p.offset_angle, p.pin_count, p.pinwheel_r, p.tooth_dif, twist)
    
    def get_normal_from_wobbles(self, draw_wobbles, twist):
        p = self.params
        return self.imported_funcs["get_normal_from_wobbles"](draw_wobbles, p.eccentricity, p.offset_angle, p.pin_count, p.pinwheel_r, p.tooth_dif, twist)
    
    def get_edge_point_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        p = self.params
        return self.imported_funcs["get_edge_from_wobbles"](draw_wobbles, p.eccentricity, input_wobbles, p.internal, p.offset_angle, p.pin_count, p.pin_r, p.pinwheel_r, p.tooth_dif, twist)
    
    def get_vel_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        p = self.params
        vel = self.imported_funcs["get_vel_from_wobbles"](draw_wobbles, p.eccentricity, p.offset_angle, p.pin_count, p.pinwheel_r, p.tooth_dif, twist)
        return np.reshape(vel, (1, 2))

    def get_nearest_starting_point_wobs(self, input_wobbles, twist, point):
        teeth = self.params.teeth()
        wobbles_per_rot = int((self.params.draw_rot_per_wobble())**-1)
        wob_step = wobbles_per_rot/teeth

        wobs = np.empty([teeth])
        dists = np.empty([teeth])

        for tooth in range(0, teeth):
            wob = tooth*wob_step
            wobs[tooth] = wob
            vec = self.get_point_from_wobbles(wob, input_wobbles, twist)
            dists[tooth] = np_vec_dist(vec, point)
        
        min_dist = dists.min()
        return wobs[np.where(dists == min_dist)[0]]
    
    def get_nearest_edge_point_wobs(self, input_wobbles, twist, point, target_dist=None, target_err = 0.0001, max_depth = 10):
        if target_dist == None:
            target_dist = self.params.pin_r

        wob = self.get_nearest_starting_point_wobs(input_wobbles, twist, point)

        iters = 0
        err = None

        while(err == None or iters < max_depth):
            iters += 1
            err_vec = point - self.get_edge_point_from_wobbles(wob, input_wobbles, twist)
            err = np_mag(err_vec)

            if err < target_dist + target_err:
                break

            self.get_vel_from_wobbles(wob, input_wobbles, twist)

            vel = self.get_vel_from_wobbles(wob, input_wobbles, twist)
            wob = wob + np.dot(vel, err_vec)/max(iters, self.params.pin_count)**(1/5)
        
        return wob
        
