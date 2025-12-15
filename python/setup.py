"""Setup script for UAStools Python package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='uastools',
    version='0.5.0',
    description='Tools for Field Based Remote Sensing Applications within Plot Based Agriculture',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Steven L. Anderson II, Seth C. Murray',
    author_email='andersst@tamu.edu',
    url='https://github.com/agryji08/UAStools',
    license='GPL-2.0',
    packages=find_packages(),
    install_requires=[
        'geopandas>=0.10.0',
        'shapely>=1.8.0',
        'numpy>=1.20.0',
        'pandas>=1.3.0',
        'matplotlib>=3.4.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    keywords='gis shapefile agriculture remote-sensing uas drone field-plots',
)
