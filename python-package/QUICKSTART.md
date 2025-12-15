# UAStools Python - Quick Start Guide

## Installation

### 1. Install Dependencies

```bash
cd python
pip install -r requirements.txt
```

Or install the package in development mode:

```bash
cd python
pip install -e .
```

### 2. Verify Installation

```python
import uastools
print(uastools.__version__)  # Should print: 0.5.0
```

## Basic Usage

### Step 1: Prepare Your Data

Create a CSV file or DataFrame with your plot layout:

```python
import pandas as pd

# Load from CSV
plot_data = pd.read_csv('your_plot_layout.csv')

# Or create manually
plot_data = pd.DataFrame({
    'Plot': [1, 2, 3, 4, 5],      # Plot numbers
    'Range': [1, 1, 1, 1, 1],      # Range (row) in field
    'Row': [1, 2, 3, 4, 5],        # Row (column) in field
    'Barcode': ['BC001', 'BC002', 'BC003', 'BC004', 'BC005']
})
```

### Step 2: Determine Your Field Coordinates

You need two UTM coordinate points:
- **Point A**: Bottom-left corner of the first plot
- **Point B**: Top-left corner in the same row as Point A

```python
# Example coordinates (UTM Zone 14N)
A_point = (746239.817, 3382052.264)  # (Easting, Northing)
B_point = (746334.224, 3382152.870)  # (Easting, Northing)
```

### Step 3: Generate Shapefiles

```python
from uastools import plotshpcreate

plotshpcreate(
    A=A_point,
    B=B_point,
    UTMzone="14",           # Your UTM zone
    Hemisphere="N",         # "N" or "S"
    infile=plot_data,
    outfile="my_field",
    field="Trial2024",      # Optional field identifier
    unit="feet"             # or "meter"
)
```

### Step 4: Check Your Output

The function creates several files:
- `Trial2024_my_field.shp` - Main shapefile
- `Trial2024_my_field_buff.shp` - Buffered shapefile
- `Trial2024_my_field_Square_plots.pdf` - Non-rotated visualization
- `Trial2024_my_field_Rotated_plots.pdf` - Rotated visualization

## Common Scenarios

### Single-Row Plots (30-inch rows, 4-foot alleys)

```python
plotshpcreate(
    A=A_point, B=B_point,
    UTMzone="14", Hemisphere="N",
    infile=plot_data,
    outfile="single_row_plots",
    field="Field1",
    nrowplot=1,          # Single row
    rowspc=2.5,          # 30 inches = 2.5 feet
    rangespc=25,         # 25-foot plots
    rowbuf=0.1,          # 0.1-foot buffer on sides
    rangebuf=2,          # 2-foot buffer (4-foot alleys / 2)
    unit="feet"
)
```

### Two-Row Plots (Combined)

```python
plotshpcreate(
    A=A_point, B=B_point,
    UTMzone="14", Hemisphere="N",
    infile=plot_data,
    outfile="tworow_combined",
    field="Field2",
    nrowplot=2,          # Two rows per plot
    multirowind=False,   # Combine into single polygon
    rowspc=2.5,
    rangespc=25,
    rowbuf=0.1,
    rangebuf=2,
    unit="feet"
)
```

### Metric Units

```python
plotshpcreate(
    A=A_point, B=B_point,
    UTMzone="14", Hemisphere="N",
    infile=plot_data,
    outfile="metric_plots",
    field="Field3",
    rowspc=0.76,         # ~30 inches in meters
    rangespc=7.62,       # ~25 feet in meters
    rowbuf=0.03,         # ~0.1 feet in meters
    rangebuf=0.61,       # ~2 feet in meters
    unit="meter"
)
```

## Running the Examples

### Basic Example

```bash
cd python/examples
python basic_example.py
```

This will create sample shapefiles with single-row plots.

### Multi-Row Example

```bash
cd python/examples
python multirow_example.py
```

This demonstrates both combined and individual multi-row plot configurations.

## Troubleshooting

### Import Error: "No module named 'geopandas'"

```bash
pip install geopandas shapely
```

### ValueError: "infile missing required columns"

Make sure your DataFrame has all required columns: 'Plot', 'Range', 'Row', 'Barcode'

### Warning: "Coordinate reference system not defined"

Add the UTMzone parameter:
```python
plotshpcreate(..., UTMzone="14", Hemisphere="N")
```

## Loading Shapefiles

### With GeoPandas

```python
import geopandas as gpd

# Load your generated shapefile
gdf = gpd.read_file('Trial2024_my_field.shp')
print(gdf.head())

# Plot it
gdf.plot()
```

### With QGIS

1. Open QGIS
2. Layer → Add Layer → Add Vector Layer
3. Browse to your .shp file
4. Click "Add"

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [CHANGELOG.md](CHANGELOG.md) for version history
- Run the test suite: `pytest tests/`
- Explore the example scripts in `examples/`

## Getting Help

- Open an issue: https://github.com/agryji08/UAStools/issues
- Check the R package documentation for conceptual background
- Email: andersst@tamu.edu

## Comparison with R Version

| Feature | R | Python |
|---------|---|--------|
| Package manager | CRAN | pip/PyPI |
| Installation | `install.packages("UAStools")` | `pip install uastools` |
| Import | `library(UAStools)` | `import uastools` |
| Vector syntax | `c(x, y)` | `(x, y)` |
| Boolean | `TRUE/FALSE` | `True/False` |
| Null value | `NULL` | `None` |
| Data frame | `data.frame()` | `pd.DataFrame()` |

Both versions produce identical shapefiles and have the same core functionality!
