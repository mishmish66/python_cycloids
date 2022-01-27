from src.utils.math_utils import *
from src.cycloid import Cycloid
import math

class Cycloid_Drawer:
    def __init__(self, cycloid, steps = 1024):
        self.steps = steps
        self.cycloid = cycloid
            
    def plot_cycloid(self, ax, input_wobbles = 0,  steps = 1024):
        points = self.get_points(input_wobbles, steps)
        ax.plot(points[0], points[1])

    def get_twist(self, input_wobbles):
        return self.cycloid.params.offset_angle - input_wobbles*self.cycloid.params.get_rot_per_wobble()*2*math.pi

    def get_point(self, draw_wobbles = 0, input_wobbles = 0, twist = None):
        if twist == None:
            twist = self.get_twist(input_wobbles)
        vec = self.cycloid.get_edge_point_from_wobbles(draw_wobbles, input_wobbles, twist)

        return vector_unwrap(vec)
            
    def get_points(self, input_wobbles = 0, steps = 1024, twist = None):
        if twist == None:
            twist = self.get_twist(input_wobbles)
        points_x = np.empty(steps)
        points_y = np.empty(steps)

        wobbles = self.cycloid.params.draw_rot_per_wobble()**-1
        wobbles_per_step = wobbles/steps

        for i in range(0, steps):
            point = self.get_point(wobbles_per_step*i, input_wobbles, twist)
            points_x[i] = point[0]
            points_y[i] = point[1]
    
        return vert([points_x, points_y])
        
    def get_normal(self, draw_wobbles = 0, input_wobbles = 0, twist = None):
        try:
            vec = self.cycloid.get_normal_from_wobbles(draw_wobbles, twist)
        except:
            vec = self.cycloid.get_normal_from_wobbles(draw_wobbles, self.get_twist(input_wobbles))

        return vector_unwrap(vec)

