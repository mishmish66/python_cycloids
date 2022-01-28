from asyncore import write
import code
from re import sub
from src.cycloid_params import Cycloid_Params
from src.cycloid_sym import Cycloid_Sym
import sympy as sp
import numpy as np
from sympy.utilities.codegen import *
from sympy.utilities.autowrap import *

def gen_funcs():

    code_gen = FCodeGen('get_cycloid_params')
    code_wrapper = F2PyCodeWrapper(code_gen, "gen")

    pin_count, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle, internal = sp.symbols('pin_count tooth_dif pinwheel_r pin_r eccentricity offset_angle internal')
    draw_wobbles, input_wobbles, twist = sp.symbols('draw_wobbles input_wobbles twist')

    cycloid_params = Cycloid_Params(pin_count, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle, internal)
    args = cycloid_params.generate_param_array()
    args = np.append(args, (draw_wobbles, input_wobbles, twist))

    cycloid = Cycloid_Sym(cycloid_params)

    get_point_expr = cycloid.get_point_from_wobbles(draw_wobbles, input_wobbles, twist)

    get_point_routine = code_gen.routine(name='get_point_from_wobbles', expr=get_point_expr)
    code_wrapper.wrap_code(get_point_routine)

    get_normal_expr = cycloid.get_normal_from_wobbles(draw_wobbles, input_wobbles, twist)

    get_normal_routine = code_gen.routine('get_normal_from_wobbles', expr=get_normal_expr)
    code_wrapper.wrap_code(get_normal_routine)

    get_edge_expr = cycloid.get_edge_point_from_wobbles(draw_wobbles, input_wobbles, twist)

    get_edge_routine = code_gen.routine('get_edge_from_wobbles', expr=get_edge_expr)
    code_wrapper.wrap_code(get_edge_routine)

    get_vel_expr = cycloid.get_vel_from_wobbles(draw_wobbles, input_wobbles, twist)

    get_vel_routine = code_gen.routine('get_vel_from_wobbles', expr=get_vel_expr)
    code_wrapper.wrap_code(get_vel_routine)