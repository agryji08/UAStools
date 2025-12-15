"""
UAStools - Tools for Field Based Remote Sensing Applications

A Python package for automating field plot shapefile (.shp) polygons
for use in data extraction of remote sensing datasets. Designed for
agricultural research applications using Unmanned Aerial System (UAS) imagery.
"""

__version__ = "0.5.0"
__author__ = "Steven L. Anderson II, Seth C. Murray"
__email__ = "andersst@tamu.edu"

from .plotshpcreate import plotshpcreate

__all__ = ['plotshpcreate']
