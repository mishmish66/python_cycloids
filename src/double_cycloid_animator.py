from concurrent.futures import thread
from matplotlib.pyplot import axes
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import patches
from src.utils.math_utils import *
from multiprocessing import Process, shared_memory
import os
import sys
from functools import reduce

class Double_Cycloid_Animator:
    def __init__(self, drawer1, drawer2, starting_wobbles = 0, wobble_step = 0.01, ending_wobbles = None):
        self.drawer1 = drawer1
        self.drawer2 = drawer2
        self.starting_wobbles = starting_wobbles
        self.wobble_step = wobble_step
        if ending_wobbles == None:
            ending_wobbles = abs(starting_wobbles + self.drawer1.cycloid.params.get_rot_per_wobble()**-1)
        self.ending_wobbles = ending_wobbles
        p1 = drawer1.cycloid.params
        p2 = drawer2.cycloid.params
        self.overall_ratio = (1 - p1.draw_rot_per_wobble())/(p2.draw_rot_per_wobble() - p1.draw_rot_per_wobble())
        pass
    
    def get_steps(self):
        return int((self.ending_wobbles - self.starting_wobbles)/self.wobble_step)

    def get_cycloid_points_from_work_piece(self, work_piece):
        wobbles = work_piece[0]
        #print("getting edge vals step " + str(work_piece[1][0]) + "/" + str(work_piece[1][1]))
        cycloid2_offset = self.get_cycloid2_offset(wobbles)

        self.drawer2.cycloid.params.offset_angle = cycloid2_offset

        c1_points = self.drawer1.get_points(wobbles, self.drawer1.steps)
        c2_points = self.drawer2.get_points(wobbles, self.drawer1.steps)

        return np.array([c1_points, c2_points])

    def get_cycloid_points_range(self, wobbles_arr):
        points = [self.get_cycloid_points_from_wobbles(wobbles) for wobbles in wobbles_arr]

        return points
    
    def get_cycloid_points_temporal(self):
        steps = self.get_steps()
        wobbles_arr = np.fromiter((step * self.wobble_step for step in range(0, steps)), float)
        cycloid2_offsets = [self.get_cycloid2_offset(wobbles) for wobbles in wobbles_arr]

        thread_count = os.cpu_count()

        work_arr = list(zip(wobbles_arr, [(i, len(wobbles_arr)) for i in range(0, len(wobbles_arr))]))

        work_chunks = np.array_split(work_arr, thread_count)

        res_chunks = [[([0.0]*self.drawer1.steps, [0.0]*self.drawer2.steps) for work_piece in work_chunk] for work_chunk in work_chunks]

        res_chunks = [np.zeros([len(work_chunk), 2, 2, self.drawer1.steps], float) for work_chunk in work_chunks]

        shm_bufs = [shared_memory.SharedMemory(create=True, size = chunk.nbytes) for chunk in res_chunks]

        def t_func(work_i):
            work_chunk = work_chunks[work_i]
            shm_a = shared_memory.SharedMemory(name = shm_bufs[work_i].name)

            res_arr = np.ndarray(res_chunks[work_i].shape, dtype=float, buffer=shm_a.buf)
            res_arr_local = [self.get_cycloid_points_from_work_piece(work_piece) for work_piece in work_chunk]
            for i in range(0, len(res_arr)): res_arr[i] = res_arr_local[i]
            shm_a.close()

        processes = [Process(target= t_func, args= (chunk_i,)) for chunk_i in range(0, thread_count)]

        for process in processes: process.start()

        for process in processes: process.join()

        chunks_with_shm = zip(res_chunks, shm_bufs)

        shared_chunks = [np.ndarray(chunk_with_shm[0].shape, dtype=float, buffer=chunk_with_shm[1].buf) for chunk_with_shm in chunks_with_shm]

        results = [[result for result in res_chunk] for res_chunk in shared_chunks]

        points1 = [[res_point[0] for res_point in res_step] for res_step in results]
        points2 = [[res_point[1] for res_point in res_step] for res_step in results]

        for shm in shm_bufs:
            shm.close()
            shm.unlink()

        return points1, points2, cycloid2_offsets

    def get_cycloid2_offset(self, input_wobbles):
        return input_wobbles * 2 * np.pi /self.overall_ratio
    
    def get_arrow_vals_temporal(self):
        steps = self.get_steps()

        p1 = self.drawer1.cycloid.params
        p2 = self.drawer2.cycloid.params

        arrows = np.zeros([steps, p1.pin_count + p2.pin_count, 2, 2])
        wasted_forces = np.zeros(steps)
        c1 = self.drawer1.cycloid
        c2 = self.drawer2.cycloid

        for step in range(0, steps):
            print("getting arrow vals step " + str(step) + "/" + str(steps))

            in_wobbles = step*self.wobble_step

            self.drawer2.cycloid.params.offset_angle = self.get_cycloid2_offset(in_wobbles)

            c2 = self.drawer2.cycloid
            p2 = c2.params

            pin_points_1 = self.drawer1.get_pin_pos_arr()
            pin_points_2 = self.drawer2.get_pin_pos_arr()

            point_norms = np.zeros([p1.pin_count + p2.pin_count, 2, 2])

            center = c1.get_wobble_center(in_wobbles)

            twist = c1.get_twist(in_wobbles)

            for n in range(0, p1.pin_count):
                point_draw_wob = c1.get_nearest_edge_point_wobs(in_wobbles, pin_points_1[n], twist)

                point = self.drawer1.get_point(point_draw_wob, in_wobbles)
                norm = c1.get_outward_normal(point_draw_wob, twist, center, vert(point))

                point_norms[n][0] = hor(point)
                point_norms[n][1] = hor(norm)

            for n in range(0, p2.pin_count):
                point_draw_wob = c2.get_nearest_edge_point_wobs(in_wobbles, pin_points_2[n])

                twist_2 = c2.get_twist(in_wobbles)

                point = self.drawer2.get_point(point_draw_wob, in_wobbles, twist_2)
                norm = c2.get_outward_normal(point_draw_wob, twist_2, center, vert(point))

                point_norms[p1.pin_count + n][0] = hor(point)
                point_norms[p1.pin_count + n][1] = hor(norm)

            arrows[step][:p1.pin_count] = c1.resolve_forces(point_norms[:p1.pin_count], in_wobbles, center, 1/self.overall_ratio)
            arrows[step][p1.pin_count:] = c2.resolve_forces(point_norms[p1.pin_count:], in_wobbles, center)

            step_arrows = arrows[step]

            step_mags = np.fromiter((np_mag(arrow[1]) for arrow in step_arrows), dtype=step_arrows.dtype)
            step_wasted = np.fromiter((np.dot(hor(np_normalize(vert(arrow[0]))), arrow[1]) for arrow in step_arrows), dtype=step_arrows.dtype)
            step_waste = np.sum(step_wasted)
            step_force = np.sum(step_mags)
            wasted_forces[step] = step_waste/step_force

        
        return (arrows, np.average(wasted_forces))


    def animate(self, fig, ax):
        points1, points2, cycloid2_offsets = self.get_cycloid_points_temporal()
        #arrow_vals_t, waste = self.get_arrow_vals_temporal()
        #print("WASTED FORCE: " + str(waste))
        steps = self.get_steps()

        p1 = self.drawer1.cycloid.params
        p2 = self.drawer2.cycloid.params

        line1, = ax.plot([], [], lw = 2)
        line2, = ax.plot([], [], lw = 2)

        objects = [line1, line2]

        pin_pos_arr1 = self.drawer1.get_pin_pos_arr()
        pin_pos_arr2 = self.drawer2.get_pin_pos_arr()

        for pin_pos in pin_pos_arr1:
            objects.append(patches.Circle((pin_pos[0], pin_pos[1]), p1.pin_r))
            ax.add_artist(objects[-1])
        
        moving_circle_start_ind = len(objects)

        for pin_pos in pin_pos_arr2:
            objects.append(patches.Circle((pin_pos[0], pin_pos[1]), p2.pin_r, animated=True))
            ax.add_artist(objects[-1])
            
        def init():
            line1.set_data([], [])
            line2.set_data([], [])
            objects.append(plt.text(-0.25, -1.25, "Overall Ratio: " + str(self.overall_ratio)))
            return objects

        def animate(step):
            this_line_1 = points1[step]
            this_line_2 = points2[step]
            line1.set_data(this_line_1[0], this_line_1[1])
            line2.set_data(this_line_2[0], this_line_2[1])
            #arrow_vals = arrow_vals_t[step]

            arrows = np.array([])

            #for n in range(0, p1.pin_count + p2.pin_count):
                #arrow = arrow_vals[n]
                #arrows = np.append(arrows, ax.quiver(arrow[0][0], arrow[0][1], arrow[1][0], arrow[1][1], scale = 1, scale_units = 'xy', width = 0.005))
            
            self.drawer2.cycloid.params.offset_angle = cycloid2_offsets[step]
            pin_pos_arr2 = self.drawer2.get_pin_pos_arr()

            for n in range(0, p2.pin_count):
                objects[n + moving_circle_start_ind].center = (pin_pos_arr2[n][0], pin_pos_arr2[n][1])

            print("frame: " + str(step) + "/" + str(steps))
            return np.append(objects, arrows)
        
        return animation.FuncAnimation(fig, animate, init_func=init, blit = True, frames = self.get_steps(), interval=1, repeat=True)