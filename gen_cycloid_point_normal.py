from asyncore import write
from re import sub
from cycloid import Cycloid
import sympy as sp
import numpy as np
from sympy.utilities.codegen import *
from sympy.utilities.autowrap import *

def gen_point_from_wobbles():

    code_gen = CCodeGen('get_cycloid_params', preprocessor_statements=["#define M_PI 3.14159265358979323846", "#include <math.h>"])
    code_wrapper = CythonCodeWrapper(code_gen, "gen")

    pin_count, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle, inverted = sp.symbols('pin_count tooth_dif pinwheel_r pin_r eccentricity offset_angle inverted')
    draw_wobbles, input_wobbles, twist = sp.symbols('draw_wobbles input_wobbles twist')

    cycloid = Cycloid(pin_count, tooth_dif, pinwheel_r, pin_r, eccentricity, offset_angle, inverted)
    args = cycloid.generate_param_array()
    args = np.append(args, (draw_wobbles, input_wobbles, twist))

    get_point_expr = cycloid.sym_get_point_from_wobbles(draw_wobbles, input_wobbles, twist)

    get_point_routine = code_gen.routine(name='get_point_from_wobbles', expr=get_point_expr)
    code_wrapper.wrap_code(get_point_routine)

    get_normal_expr = cycloid.sym_get_normal_from_wobbles(draw_wobbles, input_wobbles, twist)

    get_normal_routine = code_gen.routine('get_normal_from_wobbles', expr=get_normal_expr)
    code_wrapper.wrap_code(get_normal_routine)


gen_point_from_wobbles()