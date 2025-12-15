# Changelog

All notable changes to the UAStools Python package will be documented in this file.

## [0.5.0] - 2025-12-15

### Added
- Initial Python release of UAStools
- Full feature parity with R package version 0.5.0
- Core `plotshpcreate` function for automated shapefile generation
- Support for single-row and multi-row plot designs
- AB line rotation for proper field orientation
- Buffer zone support for precise data extraction
- UTM coordinate system support (North/South hemisphere)
- PDF visualization generation for both rotated and non-rotated plots
- Comprehensive documentation and examples

### Changed
- Migrated from R's rgdal/sp to Python's GeoPandas/Shapely
- Modern Python packaging with setup.py
- Type hints for better IDE support
- Pythonic API design with keyword arguments

### Technical Details
- Uses GeoPandas for spatial data handling
- Shapely for geometry operations
- NumPy for numerical computations
- Pandas for data manipulation
- Matplotlib for visualization

### Dependencies
- Python >= 3.8
- geopandas >= 0.10.0
- shapely >= 1.8.0
- numpy >= 1.20.0
- pandas >= 1.3.0
- matplotlib >= 3.4.0

## Future Plans

- [ ] Add support for additional plot patterns (hexagonal, etc.)
- [ ] Implement automatic coordinate detection from field boundaries
- [ ] Add GeoJSON export option
- [ ] Create interactive visualization with Plotly
- [ ] Add unit tests and continuous integration
- [ ] Create Jupyter notebook tutorials
