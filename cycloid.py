from utils import *
import math

class Cycloid:
    def __init__(self, pin_count, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle):
        self.pin_count = pin_count
        self.tooth_dif = tooth_dif
        self.pinwheel_r = pinwheel_r
        self.pin_d = pin_r
        self.eccentricity = eccentricity
        self.offset_angle = offset_angle

    def get_point_from_wobbles(self, draw_wobbles, input_wobbles):
        center_pos = np.matmul(get_rot_mat(input_wobbles*2*math.pi), vert([self.eccentricity, 0]))
        wobble_pos = np.matmul(get_rot_mat(draw_wobbles*2*math.pi + self.offset_angle), vert([-self.eccentricity, 0]))
        rotation_pos = np.matmul(get_rot_mat(draw_wobbles*2*math.pi * self.get_rot_per_wobble() + self.offset_angle), vert([self.pinwheel_r, 0]))
        return center_pos + wobble_pos + rotation_pos

    def get_rot_per_wobble(self):
        return self.tooth_dif/self.pin_count
    
    def get_points(self, steps, input_wobbles):
        pass # TODO