from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='output',
    ext_modules=cythonize(["./*.pyx"]),
)
