# UAStools - Python Version

Tools for Field Based Remote Sensing Applications within Plot Based Agriculture

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--2.0-green.svg)](https://www.gnu.org/licenses/gpl-2.0.html)

## Overview

UAStools is a Python package that provides functions to automate field plot shapefile (.shp) polygons for use in data extraction of remote sensing datasets. It's designed for agricultural research applications using Unmanned Aerial System (UAS) imagery.

This is the Python port of the original R package, utilizing modern geospatial libraries like GeoPandas and Shapely.

## Features

- 🌾 **Automated Plot Shapefile Generation**: Create precise field plot boundaries from simple coordinate inputs
- 📐 **AB Line Rotation**: Automatically rotate polygons to match field orientation
- 🔄 **Multi-row Plot Support**: Handle single or multi-row plot designs with flexible configurations
- 📊 **Visualization**: Generate PDF plots for visual verification of both rotated and non-rotated layouts
- 🎯 **Buffer Zones**: Create buffered plot boundaries for precise data extraction
- 🌍 **UTM Projection Support**: Full support for UTM coordinate systems (North/South hemisphere)

## Installation

### From source:

```bash
cd python
pip install -e .
```

### Requirements

- Python >= 3.8
- geopandas >= 0.10.0
- shapely >= 1.8.0
- numpy >= 1.20.0
- pandas >= 1.3.0
- matplotlib >= 3.4.0

## Quick Start

```python
import pandas as pd
from uastools import plotshpcreate

# Create sample plot layout data
infile = pd.DataFrame({
    'Plot': range(1, 101),
    'Range': [i // 10 + 1 for i in range(100)],
    'Row': [i % 10 + 1 for i in range(100)],
    'Barcode': [f'BC{i:03d}' for i in range(1, 101)]
})

# Generate shapefiles
plotshpcreate(
    A=(746239.817, 3382052.264),  # Bottom left corner (Easting, Northing)
    B=(746334.224, 3382152.870),  # Top left corner (Easting, Northing)
    UTMzone="14",
    Hemisphere="N",
    infile=infile,
    outfile="my_plots",
    field="CS17-G2FE",
    nrowplot=1,
    rowspc=2.5,      # Row spacing in feet (30-inch rows)
    rangespc=25,     # Plot length in feet
    rowbuf=0.1,      # Row buffer in feet
    rangebuf=2,      # Range buffer in feet (4-foot alleys)
    unit="feet",
    SquarePlot=True,
    RotatePlot=True
)
```

## Parameters

### Required Parameters

- `A`: Tuple of (Easting, Northing) UTM coordinates for bottom-left corner of first plot
- `B`: Tuple of (Easting, Northing) UTM coordinates for top-left corner in same row as A
- `infile`: pandas DataFrame with columns: 'Plot', 'Range', 'Row', 'Barcode'
- `outfile`: Output filename prefix (without .shp extension)

### Optional Parameters

- `UTMzone`: UTM zone number (e.g., "14")
- `Hemisphere`: "N" or "S" for Northern or Southern hemisphere
- `nrowplot`: Number of adjacent rows per plot (default: 1)
- `multirowind`: If True, create separate polygons for each row in multi-row plots
- `rowspc`: Row spacing (default: 2.5 feet = 30-inch rows)
- `rowbuf`: Buffer distance removed from row edges (default: 0.1 feet)
- `rangespc`: Plot length including half-alleys (default: 25 feet)
- `rangebuf`: Buffer distance removed from range edges (default: 2 feet)
- `unit`: "feet" or "meter" (default: "feet")
- `SquarePlot`: Generate PDF of non-rotated plots (default: True)
- `RotatePlot`: Generate PDF of rotated plots (default: True)

## Input Data Format

The `infile` DataFrame must contain these columns:

- **Plot**: Unique plot identifier (integer)
- **Range**: Range (row) number in the field layout
- **Row**: Row (column) number in the field layout
- **Barcode**: Unique identifier for each plot entry (string)

Example:
```python
infile = pd.DataFrame({
    'Plot': [1, 1, 2, 2, 3, 3],
    'Range': [1, 1, 1, 1, 1, 1],
    'Row': [1, 2, 3, 4, 5, 6],
    'Barcode': ['P001_R1', 'P001_R2', 'P002_R1', 'P002_R2', 'P003_R1', 'P003_R2']
})
```

## Output Files

The function generates:

1. **Main shapefile**: `{field}_{outfile}.shp` (and associated .shx, .dbf, .prj files)
2. **Buffered shapefile**: `{field}_{outfile}_buff.shp` (with buffer zones applied)
3. **Square plot PDF** (optional): `{field}_{outfile}_Square_plots.pdf`
4. **Rotated plot PDF** (optional): `{field}_{outfile}_Rotated_plots.pdf`

## Use Cases

### Single-Row Plots

```python
plotshpcreate(
    A=(x1, y1), B=(x2, y2),
    infile=data,
    outfile="single_row",
    nrowplot=1  # Default
)
```

### Multi-Row Plots (Combined)

```python
plotshpcreate(
    A=(x1, y1), B=(x2, y2),
    infile=data,
    outfile="multirow_combined",
    nrowplot=2,
    multirowind=False  # Combine adjacent rows into single polygon
)
```

### Multi-Row Plots (Individual)

```python
plotshpcreate(
    A=(x1, y1), B=(x2, y2),
    infile=data,
    outfile="multirow_individual",
    nrowplot=2,
    multirowind=True  # Each row gets unique identifier
)
```

### Metric Units

```python
plotshpcreate(
    A=(x1, y1), B=(x2, y2),
    infile=data,
    outfile="metric_plots",
    rowspc=0.76,    # meters (30-inch rows)
    rangespc=7.62,  # meters (25 feet)
    rowbuf=0.03,    # meters
    rangebuf=0.61,  # meters
    unit="meter"
)
```

## Differences from R Version

The Python version maintains the same core functionality as the R package but with some modernizations:

- Uses **GeoPandas** instead of rgdal/sp (which are deprecated)
- More Pythonic API with keyword arguments
- Improved error messages and validation
- Type hints for better IDE support
- Modern matplotlib for visualizations

## Migration Guide (R to Python)

| R Syntax | Python Syntax |
|----------|---------------|
| `A=c(x,y)` | `A=(x,y)` |
| `TRUE/FALSE` | `True/False` |
| `data.frame()` | `pd.DataFrame()` |
| `NULL` | `None` |
| Vector indexing `[1]` | Zero-based indexing `[0]` |

## License

GPL-2.0 - see LICENSE file for details

## Authors

- Steven L. Anderson II (andersst@tamu.edu)
- Seth C. Murray

## Citation

If you use UAStools in your research, please cite:

```
Anderson, S.L., II, & Murray, S.C. (2025). UAStools: Tools for Field Based
Remote Sensing Applications within Plot Based Agriculture. Python package
version 0.5.0. https://github.com/agryji08/UAStools
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For bug reports and feature requests, please use the [GitHub issue tracker](https://github.com/agryji08/UAStools/issues).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

### Version 0.5.0 (2025-12-15)

- Initial Python release
- Full feature parity with R version 0.5.0
- Migration to modern geospatial stack (GeoPandas, Shapely)
- Improved documentation and examples
