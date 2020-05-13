from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('imagetitler/gui.py', base=base, targetName = 'image-titler-gui')
]

setup(name='Image Titler',
      version = '2.4.0',
      description = 'An image processing utility which provides options for generating thumbnails for various social media platforms.',
      options = dict(build_exe = buildOptions),
      executables = executables)
