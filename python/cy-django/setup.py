from distutils.core import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("*", ["*.pyx"],
              include_dirs=['cy_migrations/upstream', 'cy_migrations/upstream/operations'])
]
setup(
    ext_modules=cythonize(['cy_migrations/upstream/*.pyx', 'cy_migrations/upstream/operations/*.pyx',
                           'cy_migrations/management/commands/*.pyx']),
    packages=['cy_migrations']
)