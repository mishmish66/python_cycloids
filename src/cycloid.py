from os import path
from matplotlib.pyplot import draw
import numpy as np
from src.utils.func_utils import get_funcs
from src.utils.math_utils import (np_mag, np_vec_dist, get_np_rot_mat, np_normalize, vert, hor)

class Cycloid:
    def __init__(self, cycloid_params):
        self.params = cycloid_params
        self.imported_funcs = get_funcs()

    def get_twist(self, input_wobbles):
        p = self.params
        #offset = p.offset_angle / p.draw_rot_per_wobble() * p.get_rot_per_wobble()
        #return offset - input_wobbles*p.get_rot_per_wobble()*2*np.pi
        return -input_wobbles*p.get_rot_per_wobble()*2*np.pi
    
    def get_wobble_center(self, input_wobbles):
        return np.matmul(get_np_rot_mat(input_wobbles*2*np.pi), vert([self.params.eccentricity, 0]))
    
    def resolve_forces(self, disp_arrows, wob, center = None):
        #if center == None:
        #    center = self.get_wobble_center(wob)
        center_vel = hor(self.get_vel_from_wobbles(wob, center))
        center = hor(center)

        contributions = np.fromiter((np.dot(center_vel, arrow[1]) for arrow in disp_arrows), dtype=disp_arrows.dtype)
        if self.params.internal:
            contributions = np.fromiter((np.max([-rat, 0]) for rat in contributions), dtype=disp_arrows.dtype)
        else:
            contributions = np.fromiter((np.max([rat, 0]) for rat in contributions), dtype=disp_arrows.dtype)

        contributions = contributions/np.sum(contributions)

        resolved = np.empty([len(disp_arrows), 2, 2])
        for n in range(0, len(disp_arrows)):
            arrow = disp_arrows[n]
            contribution = contributions[n]
            resolved[n] = [arrow[0], contribution * arrow[1]]

        return resolved
        
    def get_overlay_twist_and_draw_wobbles(self, draw_wobbles, twist):
        p = self.params # TODO make this actually work
        return (draw_wobbles, twist)
    
    def get_point_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        p = self.params
        overlay_wobbles, overlay_twist = self.get_overlay_twist_and_draw_wobbles(draw_wobbles, twist)
        return self.imported_funcs["get_point_from_wobbles"](overlay_wobbles, p.eccentricity, input_wobbles, p.offset_angle, p.pin_count, p.pinwheel_r, p.tooth_dif, overlay_twist)
    
    def get_normal_from_wobbles(self, draw_wobbles, twist):
        p = self.params
        overlay_wobbles, overlay_twist = self.get_overlay_twist_and_draw_wobbles(draw_wobbles, twist)
        return self.imported_funcs["get_normal_from_wobbles"](overlay_wobbles, p.eccentricity, p.offset_angle, p.pin_count, p.pinwheel_r, p.tooth_dif, overlay_twist)
    
    def get_outward_normal(self, draw_wobbles, twist, center, point):
        p = self.params
        norm = self.get_normal_from_wobbles(draw_wobbles, twist)
        pos = point + norm
        neg = point - norm
        if np_vec_dist(pos, center) > np_vec_dist(neg, center):
            return norm
        else:
            return -norm
    
    def get_vel_from_wobbles(self, wobbles, center):
        p = self.params
        #if center == None:
        #    center = self.get_wobble_center(wobbles)
        
        return np_normalize(np.matmul(get_np_rot_mat(np.pi/2), center))
        
    
    def get_edge_point_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        p = self.params
        overlay_wobbles, overlay_twist = self.get_overlay_twist_and_draw_wobbles(draw_wobbles, twist)
        return self.imported_funcs["get_edge_from_wobbles"](overlay_wobbles, p.eccentricity, input_wobbles, p.internal, p.offset_angle, p.pin_count, p.pin_r, p.pinwheel_r, p.tooth_dif, overlay_twist)
    
    def get_draw_vel_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        p = self.params
        vel = self.imported_funcs["get_draw_vel_from_wobbles"](draw_wobbles, p.eccentricity, p.offset_angle, p.pin_count, p.pinwheel_r, p.tooth_dif, twist)
        return np.reshape(vel, (1, 2))

    def get_point_vel_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        p = self.params
        return self.imported_funcs["get_point_vel_from_wobbles"](p.eccentricity, input_wobbles)

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

            self.get_draw_vel_from_wobbles(wob, input_wobbles, twist)

            vel = self.get_draw_vel_from_wobbles(wob, input_wobbles, twist)
            wob = wob + np.dot(vel, err_vec)/max(iters, self.params.pin_count)**(1/5)
        
        return wob
        
