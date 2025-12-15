"""
Example of multi-row plot generation.

This example shows how to create shapefiles for multi-row plots,
both combined (single polygon per plot) and individual (separate
polygons for each row within a plot).
"""

import pandas as pd
from uastools import plotshpcreate

# Create sample plot data for 2-row plots
# Each plot spans 2 adjacent rows
plot_data = pd.DataFrame({
    'Plot': [i for i in range(1, 26) for _ in range(2)],  # 25 plots, 2 rows each
    'Range': [i // 5 + 1 for i in range(50)],  # 10 ranges
    'Row': [i % 5 + 1 for i in range(50)],     # 5 columns (but 2 rows per plot)
    'Barcode': [f'ENTRY_{i:03d}' for i in range(1, 51)]
})

print("Multi-row plot data:")
print(plot_data.head(10))
print(f"\nTotal entries: {len(plot_data)}")
print(f"Unique plots: {plot_data['Plot'].nunique()}")

# Field coordinates
A_point = (746239.817, 3382052.264)
B_point = (746334.224, 3382152.870)

# Example 1: Combined multi-row plots
# Creates one polygon encompassing both rows of each plot
print("\n" + "="*60)
print("Example 1: Combined multi-row plots")
print("="*60)

plotshpcreate(
    A=A_point,
    B=B_point,
    UTMzone="14",
    Hemisphere="N",
    infile=plot_data,
    outfile="multirow_combined",
    field="Trial2017",
    nrowplot=2,          # 2-row plots
    multirowind=False,   # Combine rows into single polygon
    rowspc=2.5,
    rowbuf=0.1,
    rangespc=25,
    rangebuf=2,
    unit="feet",
    SquarePlot=True,
    RotatePlot=True
)

print("Created combined multi-row shapefiles")

# Example 2: Individual multi-row plots
# Creates separate polygons for each row, with unique IDs
print("\n" + "="*60)
print("Example 2: Individual multi-row plots")
print("="*60)

plotshpcreate(
    A=A_point,
    B=B_point,
    UTMzone="14",
    Hemisphere="N",
    infile=plot_data,
    outfile="multirow_individual",
    field="Trial2017",
    nrowplot=2,          # 2-row plots
    multirowind=True,    # Keep rows separate with unique IDs
    rowspc=2.5,
    rowbuf=0.1,
    rangespc=25,
    rangebuf=2,
    unit="feet",
    SquarePlot=True,
    RotatePlot=True
)

print("Created individual multi-row shapefiles")
print("\nDone! Check the output files for both examples.")
