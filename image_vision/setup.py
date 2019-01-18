import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["scipy.fftpack", "scipy.ndimage", "skimage.io", "numpy.core", "skimage.util", "skimage.color", "cytoolz.functoolz", "cytoolz", # Try to remove: "skimage.util", "skimage.color", "cytoolz.functoolz",
                                  "plugins", "core"],
                     "excludes": ["tkinter",
                                  "scipy.spatial.cKDTree"],  # to fix current bug
                     "includes": ["numpy", "scipy.sparse.csgraph._validation"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"
#     print("Win32GUI")
# else:
#     print('base = None')

setup(name="ImageVision",
      version="0.1",
      description="Image segmentator for neural networks.",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
