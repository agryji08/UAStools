# UAStools

**Tools for Field Based Remote Sensing Applications within Plot Based Agriculture**

[![R Package](https://img.shields.io/badge/R-v0.5.0-blue.svg)](r-package/)
[![Python Package](https://img.shields.io/badge/Python-v0.5.0-green.svg)](python-package/)
[![License](https://img.shields.io/badge/license-GPL--2.0-orange.svg)](LICENSE)

---

## 📋 Overview

UAStools is a comprehensive toolkit for automating field plot shapefile (.shp) polygon generation for use in data extraction of remote sensing datasets. Designed specifically for agricultural research applications using Unmanned Aerial System (UAS) imagery.

This repository contains **two implementations** with **full feature parity**:
- **[R Package](r-package/)** - Traditional R implementation using modern `sf` package
- **[Python Package](python-package/)** - Python implementation using `GeoPandas` and `Shapely`

Both versions produce **identical shapefiles** and can be used interchangeably based on your workflow preferences.

---

## 🎯 Key Features

- 🌾 **Automated Plot Boundary Generation**: Create precise field plot boundaries from simple coordinate inputs
- 📐 **AB Line Rotation**: Automatically rotate polygons to match field orientation using AB reference line
- 🔄 **Multi-row Plot Support**: Handle single or multi-row plot designs with flexible configurations
- 📊 **Visual Verification**: Generate PDF plots for visual verification of both rotated and non-rotated layouts
- 🎯 **Buffer Zones**: Create buffered plot boundaries for precise data extraction
- 🌍 **UTM Projection Support**: Full support for UTM coordinate systems (North/South hemisphere)
- 🔍 **Stagger Support**: Handle staggered planting patterns common in field trials

---

## 📦 Installation & Quick Start

### R Package

```r
# Install from source
install.packages("devtools")
devtools::install_github("agryji08/UAStools", subdir = "r-package")

# Load package
library(UAStools)

# Basic usage
plotshpcreate(
  A = c(746239.817, 3382052.264),
  B = c(746334.224, 3382152.870),
  UTMzone = "14",
  Hemisphere = "N",
  infile = your_data,
  outfile = "my_plots",
  field = "Trial2024"
)
```

📖 **[Full R Documentation →](r-package/)**

---

### Python Package

```bash
# Install
cd python-package
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

```python
import pandas as pd
from uastools import plotshpcreate

# Basic usage
plotshpcreate(
    A=(746239.817, 3382052.264),
    B=(746334.224, 3382152.870),
    UTMzone="14",
    Hemisphere="N",
    infile=your_dataframe,
    outfile="my_plots",
    field="Trial2024"
)
```

📖 **[Full Python Documentation →](python-package/)**

📖 **[Python Quick Start Guide →](python-package/QUICKSTART.md)**

---

## 🔄 Which Version Should I Use?

| Consideration | R Package | Python Package |
|--------------|-----------|----------------|
| **Your workflow is primarily in...** | R, RStudio | Python, Jupyter |
| **Team uses...** | R for statistics | Python for GIS |
| **Integration with...** | ggplot2, tidyverse | matplotlib, scikit-learn |
| **Package ecosystem** | CRAN packages | PyPI packages |
| **GIS tools** | sf, terra, raster | GeoPandas, Shapely, Rasterio |

Both produce **identical shapefiles** - choose based on your existing workflow!

---

## 📊 Repository Structure

```
UAStools/
├── README.md                    # This file
├── LICENSE                      # GPL-2.0 License
├── .gitignore                   # Git ignore rules
│
├── r-package/                   # R Package
│   ├── DESCRIPTION             # R package metadata
│   ├── NAMESPACE               # R namespace
│   ├── NEWS.md                 # R version changelog
│   ├── R/                      # R source code
│   │   └── plotshpcreate.R
│   ├── man/                    # R documentation
│   ├── data/                   # Sample datasets
│   │   ├── SampleInfile.rda
│   │   └── SampleInfile_Subset.rda
│   └── inst/                   # Additional files
│       └── CITATION
│
└── python-package/              # Python Package
    ├── setup.py                # Python package configuration
    ├── requirements.txt        # Python dependencies
    ├── README.md               # Python-specific docs
    ├── QUICKSTART.md           # Quick start guide
    ├── CHANGELOG.md            # Python version changelog
    ├── uastools/               # Python source code
    │   ├── __init__.py
    │   └── plotshpcreate.py
    ├── examples/               # Example scripts
    │   ├── basic_example.py
    │   └── multirow_example.py
    └── tests/                  # Unit tests
        └── test_plotshpcreate.py
```

---

## 🚀 How It Works

UAStools uses an **AB line reference system** to properly orient field plots:

1. **Define Reference Points**: Specify Point A (bottom-left) and Point B (top-left) of your field
2. **Provide Plot Layout**: Supply a data table with plot numbers, ranges, and rows
3. **Configure Dimensions**: Set row spacing, plot length, and buffer zones
4. **Generate Shapefiles**: Automatically creates rotated, georeferenced plot boundaries

### Input Requirements

Both packages require the same input data structure:

| Column | Description | Example |
|--------|-------------|---------|
| `Plot` | Unique plot identifier | 1, 2, 3, ... |
| `Range` | Range (row) number in field layout | 1, 2, 3, ... |
| `Row` | Row (column) number in field layout | 1, 2, 3, ... |
| `Barcode` | Unique identifier for each entry | "BC001", "BC002", ... |

### Output Files

Both versions generate:
- **Main shapefile**: `{field}_{outfile}.shp` (+ .shx, .dbf, .prj)
- **Buffered shapefile**: `{field}_{outfile}_buff.shp`
- **Square plot PDF**: Non-rotated visualization (optional)
- **Rotated plot PDF**: Field-oriented visualization (optional)

---

## 📚 Documentation

### General Documentation
- [Main README](README.md) - This file
- [LICENSE](LICENSE) - GPL-2.0 License
- [Citation Information](r-package/inst/CITATION)

### R Package
- [R Package Documentation](r-package/)
- [R Package NEWS](r-package/NEWS.md)
- [R Function Documentation](r-package/man/)

### Python Package
- [Python Package Documentation](python-package/)
- [Python Quick Start](python-package/QUICKSTART.md)
- [Python Changelog](python-package/CHANGELOG.md)
- [Python Examples](python-package/examples/)
- [Python Tests](python-package/tests/)

---

## 🔬 Use Cases

- **Agricultural Field Trials**: Automated plot boundary creation for breeding programs
- **High-Throughput Phenotyping**: Extract plot-level data from UAS imagery
- **Precision Agriculture**: Map management zones and prescription areas
- **Remote Sensing Research**: Automate data extraction pipelines
- **GIS Analysis**: Generate standardized plot geometries for spatial analysis

---


---

## 📝 Version History

### Version 0.5.0 (2025-12-15)

**R Package:**
- ✅ Migrated from deprecated `rgdal/sp` to modern `sf` package
- ✅ Updated for CRAN compatibility
- ✅ Fixed documentation to comply with CRAN policies
- ✅ Improved package metadata

**Python Package:**
- ✨ Initial Python release
- ✅ Full feature parity with R version
- ✅ Modern geospatial stack (GeoPandas, Shapely)
- ✅ Comprehensive documentation and examples
- ✅ Unit tests with pytest

**Repository:**
- 🏗️ Restructured as monorepo with `r-package/` and `python-package/`
- 📚 Unified documentation
- 👥 Updated author list

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

**For R package:**
```r
devtools::load_all("r-package")
devtools::test("r-package")
devtools::check("r-package")
```

**For Python package:**
```bash
cd python-package
pip install -e ".[dev]"
pytest tests/
```

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/agryji08/UAStools/issues)
- **Email**:
  - Zhongjie Ji: zji7@unl.edu
- **Documentation**: See package-specific READMEs

---

## 📜 License

GPL-2.0 - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Repository**: https://github.com/agryji08/UAStools
- **R Package**: [r-package/](r-package/)
- **Python Package**: [python-package/](python-package/)

---

<p align="center">
  <strong>Built with ❤️ for the agricultural research community</strong>
</p>

<p align="center">
  <sub>R Package | Python Package | Open Source | GPL-2.0</sub>
</p>
