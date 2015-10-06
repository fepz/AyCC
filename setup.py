from cx_Freeze import setup, Executable
from os.path import dirname

import scipy
includefiles_list=[]
scipy_path = dirname(scipy.__file__)
includefiles_list.append(scipy_path)

import lib2to3
lib2to3_path = dirname(lib2to3.__file__)
includefiles_list.append(lib2to3_path)

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(packages = [], excludes = ['tcl','matplotlib'], include_msvcr = [], include_files=includefiles_list)

base = 'Console'

executables = [
    Executable('graphs_2.py', base=base, targetName = 'aycc.exe')
]

setup(name='aycc',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
