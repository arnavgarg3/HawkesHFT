from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'hawkes_engine',
        ['src/engine.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++'
    ),
]

setup(
    name='hawkes_engine',
    ext_modules=ext_modules,
)   