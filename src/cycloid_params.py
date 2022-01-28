import numpy as np

class Cycloid_Params:
    def __init__(self, pin_count, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle, internal):
        self.pin_count = pin_count
        self.tooth_dif = tooth_dif
        self.pinwheel_r = pinwheel_r
        self.pin_r = pin_r
        self.eccentricity = eccentricity
        self.offset_angle = offset_angle
        self.internal = internal

    def draw_rot_per_wobble(self):
        return -self.tooth_dif/self.pin_count
    
    def get_rot_per_wobble(self):
        return -self.tooth_dif/(self.pin_count + self.tooth_dif)
    
    def generate_param_array(self):
        return np.array([self.pin_count, self.tooth_dif, self.pinwheel_r, self.pin_r, self.eccentricity, self.offset_angle, self.internal])
    
    def teeth(self):
        return self.pin_count + self.tooth_dif
