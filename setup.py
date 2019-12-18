import sys
import numpy as np
import setuptools
from distutils.core import setup
from distutils.extension import Extension

package_name = 'geodisTK'
module_name  = 'geodesic_distance'
version      = sys.version[0]
wrap_source  = './cpp/wrap_py{0:}.cpp'.format(version)
module1      = Extension(module_name,
                    include_dirs = [np.get_include(), './cpp'],
                    sources = ['./cpp/util.cpp', 
                               './cpp/geodesic_distance_2d.cpp', 
                               './cpp/geodesic_distance_3d.cpp', 
                               './cpp/geodesic_distance.cpp',
                               wrap_source])

# Get the summary
description = 'An open-source toolkit to calculate geodesic distance' + \
              ' for 2D and 3D images'

# Get the long description
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name    = package_name,
    version = "0.1.5.2",
    author  ='Guotai Wang',
    author_email = 'wguotai@gmail.com',
    description  = description,
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url      = 'https://github.com/taigw/geodesic_distance',
    license  = 'MIT',
    packages = setuptools.find_packages(),
    ext_modules = [module1],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    python_requires = '>=3.6',
)

# to build, run python stup.py build or python setup.py build_ext --inplace
# to install, run python setup.py install
