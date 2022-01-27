import os
import importlib
from src.gen_funcs import gen_funcs
from inspect import isroutine
from pathlib import Path

def get_funcs():
    if funcs_need_reloading():
        gen_funcs()
    
    mod_arr = find_generated_mods()

    return get_funcs_from_mods(mod_arr)


def funcs_need_reloading():
    return True # TODO make this actually do stuff

def find_generated_mods():
    dir_path = Path(os.path.realpath(__file__)).parents[2].joinpath("gen")
    func_files = []

    for file in dir_path.iterdir():
        if file.match("*.so"):
            func_files.append(file)
    return func_files
    
def get_funcs_from_mods(mod_files):
    funcs = {}
    for mod_file in mod_files:
        mod = importlib.import_module(str(mod_file.name).split('.')[0], str(mod_file.parent))
        funcs = funcs | get_funcs_from_mod(mod)
    return funcs

def get_funcs_from_mod(mod):
    funcs = {}
    for attr_name in dir(mod):
        attr = getattr(mod, attr_name)
        if str(type(attr)) == '<class \'fortran\'>':
            funcs[attr_name] = attr
    return funcs