from src.utils.math_utils import *
import sympy as sp
from sympy.logic.boolalg import (Not, Xor)

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
    
    def get_edge_point_from_wobbles(self, draw_wobbles, input_wobbles, twist):
        normal_vec = self.get_normal_from_wobbles(draw_wobbles, input_wobbles, twist)
        center = self.get_wobble_center(input_wobbles)
        point = self.get_point_from_wobbles(draw_wobbles, input_wobbles, twist)

        vec1 = point + normal_vec * self.params.pin_r

        vec2 = point - normal_vec * self.params.pin_r

        dvec1 = vec1-center
        dvec2 = vec2-center

        d1 = vector_magnitude(dvec1)
        d2 = vector_magnitude(dvec2)

        cmp = sp.GreaterThan(d2, d1)

        cond = Xor(cmp, self.params.internal > 0)

        x = sp.Piecewise((vec1[0], cond), (vec2[0], True))
        y = sp.Piecewise((vec1[1], cond), (vec2[1], True))

        return sp.Matrix([x, y])

    def get_normal_from_wobbles(self, draw_wobbles, input_wobbles, twist):

        point = self.get_point_from_wobbles(draw_wobbles, input_wobbles, twist)
        point = sp.simplify(point)

        vel = sp.diff(point, draw_wobbles)
        tan = vector_normalize(vel)

        curv = sp.diff(tan, draw_wobbles)
        norm = vector_normalize(curv)

        return norm