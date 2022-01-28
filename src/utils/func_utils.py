import os
import importlib
from src.gen_funcs import gen_funcs
from inspect import isroutine
from pathlib import Path
import sys

def get_funcs():
    if funcs_need_reloading():
        gen_funcs()
    
    mod_arr = find_generated_mods()

    return get_funcs_from_mods(mod_arr)


def funcs_need_reloading():
    gen = get_gen_folder()
    src = gen.parent.joinpath("src")

    try:
        gen_mtime = gen.stat().st_mtime
    except(FileNotFoundError):
        return True
    
    for file in src.iterdir():
        if file.stat().st_mtime > gen_mtime:
            return True
            
    return False

def get_gen_folder():
    return Path(os.path.realpath(__file__)).parents[2].joinpath("gen")

def find_generated_mods():
    dir_path = get_gen_folder()
    func_files = []

    for file in dir_path.iterdir():
        if file.match("*.so"):
            func_files.append(file)
    return func_files
    
def get_funcs_from_mods(mod_files):
    funcs = {}
    for mod_file in mod_files:
        sys.path.insert(0, str(mod_file.parent))
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