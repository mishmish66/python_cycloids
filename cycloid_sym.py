from math_utils import *
import sympy as sp

class Cycloid_Sym:
    def __init__(self, cycloid_params):
        self.params = cycloid_params
    
    def get_wobble_center(self, input_wobbles):
        return sp.MatMul(get_rot_mat(input_wobbles*2*sp.pi), sp.Matrix([self.params.eccentricity, 0]))

    def get_point_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        center_pos = self.get_wobble_center(input_wobbles)
        wobble_pos = sp.MatMul(get_rot_mat(draw_wobbles*2*sp.pi + self.params.offset_angle + twist), sp.Matrix([-self.params.eccentricity, 0]))
        rotation_pos = sp.MatMul(get_rot_mat(draw_wobbles*2*sp.pi * self.params.draw_rot_per_wobble() + self.params.offset_angle + twist), sp.Matrix([self.params.pinwheel_r, 0]))
        return center_pos + wobble_pos + rotation_pos
    
    def get_edge_point_from_wobbles(self, draw_wobbles, input_wobbles, twist, normal = None):
        center = self.get_wobble_center(input_wobbles)
        point = self.get_point_from_wobbles(draw_wobbles, input_wobbles, twist)

        v1 = point + normal * self.params.pin_r
        v1 = sp.simplify(v1)

        v2 = point - normal * self.params.pin_r
        v2 = sp.simplify(v2)

        d1 = vectors_distance(v1, center)
        d2 = vectors_distance(v2, center)

        return sp.Piecewise((v1, d1 > d2), (v2, True))

    def get_normal_from_wobbles(self, draw_wobbles, input_wobbles, twist):

        point = self.get_point_from_wobbles(draw_wobbles, input_wobbles, twist)
        point = sp.simplify(point)

        vel = sp.diff(point, draw_wobbles)
        tan = vector_normalize(vel)

        curv = sp.diff(tan, draw_wobbles)
        norm = vector_normalize(curv)

        return norm