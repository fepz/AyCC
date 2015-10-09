#
# Generate native binary executable from Python code.
#
from cx_Freeze import setup, Executable
from os.path import dirname

includefiles_list=[]

import scipy
scipy_path = dirname(scipy.__file__)
includefiles_list.append(scipy_path)

import matplotlib
matplotlib_path = dirname(matplotlib.__file__)
includefiles_list.append(matplotlib_path)

import lib2to3
lib2to3_path = dirname(lib2to3.__file__)
includefiles_list.append(lib2to3_path)

import tkinter.filedialog
tkinter = dirname(tkinter.__file__)
includefiles_list.append(tkinter)

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(packages = [], 
                    excludes = [], 
                    include_msvcr = [], 
                    include_files=includefiles_list)

base = 'Console'

executables = [ Executable('aycc.py', base=base, targetName = 'aycc.exe') ]

setup(name='aycc',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
