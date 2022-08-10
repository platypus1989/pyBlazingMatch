import sys

from pybind11 import get_cmake_dir
# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, Extension, find_packages

__version__ = "0.0.1"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

dependencies = [
    'statsmodels',
    'pandas',
    'numpy'
  ]

ext_modules = [
    Pybind11Extension("cppmodule",
        ["blazingMatch/src/main.cpp"],
        # Example: passing in the version to the compiled code
        define_macros = [('VERSION_INFO', __version__)],
        ),
]

setup(
    name="blazingMatch",
    version=__version__,
    author="Chuan Wang",
    author_email="wangchuan1989@gmail.com",
    url="https://github.com/platypus1989/pyBlazingMatch",
    description="blazing fast propensity score matching with Python",
    long_description="",
    packages = find_packages(),
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
    include_package_data=True,
    package_data={'': ['data/*.csv']},
    install_requires=dependencies,
)
