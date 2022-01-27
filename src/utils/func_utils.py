import os
import importlib
from src.gen_funcs import gen_funcs
from inspect import isroutine

def get_funcs():
    if funcs_need_reloading():
        gen_funcs()
    
    pyx_arr = find_pyx()

    return get_funcs_from_mods(pyx_arr)


def funcs_need_reloading():
    return True # TODO make this actually do stuff

def find_pyx():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_path + "/../../gen"
    func_files = []

    for _, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.pyx'):
                func_files.append(file[0:-4])
    return func_files
    
def get_funcs_from_mods(mod_file_arr):
    funcs = {}
    for mod_file in mod_file_arr:
        mod = importlib.import_module(mod_file)
        funcs = funcs | get_funcs_from_mod(mod)
    return funcs

def get_funcs_from_mod(mod):
    funcs = {}
    for attr_name in dir(mod):
        attr = getattr(mod, attr_name)
        if isroutine(attr):
            funcs[attr_name] = attr
    return funcs