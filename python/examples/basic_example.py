"""
Basic example of using UAStools to create field plot shapefiles.

This example demonstrates single-row plot generation with visualization.
"""

import pandas as pd
from uastools import plotshpcreate

# Create sample plot data
# In a real scenario, you would load this from a CSV file
plot_data = pd.DataFrame({
    'Plot': list(range(1, 51)) * 2,  # 50 plots, 2 rows each
    'Range': [i // 10 + 1 for i in range(100)],  # 10 ranges
    'Row': [i % 10 + 1 for i in range(100)],  # 10 rows
    'Barcode': [f'PLOT_{i:03d}' for i in range(1, 101)]
})

print("Sample plot data:")
print(plot_data.head(10))
print(f"\nTotal entries: {len(plot_data)}")
print(f"Unique plots: {plot_data['Plot'].nunique()}")
print(f"Ranges: {plot_data['Range'].nunique()}")
print(f"Rows: {plot_data['Row'].nunique()}")

# Define field corner coordinates (UTM)
# Point A: Bottom-left corner of first plot
A_point = (746239.817, 3382052.264)

# Point B: Top-left corner in same row as A
B_point = (746334.224, 3382152.870)

# Generate shapefiles
print("\nGenerating shapefiles...")
plotshpcreate(
    A=A_point,
    B=B_point,
    UTMzone="14",
    Hemisphere="N",
    infile=plot_data,
    outfile="example_plots",
    field="CS17-G2FE",
    nrowplot=1,          # Single row plots
    multirowind=False,
    rowspc=2.5,          # 30-inch row spacing (in feet)
    rowbuf=0.1,          # Small buffer on row edges
    rangespc=25,         # 25-foot plot length
    rangebuf=2,          # 2-foot buffer (4-foot alleys)
    unit="feet",
    SquarePlot=True,     # Generate non-rotated visualization
    RotatePlot=True      # Generate rotated visualization
)

print("\nDone! Check the output files:")
print("  - CS17-G2FE_example_plots.shp (main shapefile)")
print("  - CS17-G2FE_example_plots_buff.shp (buffered shapefile)")
print("  - CS17-G2FE_example_plots_Square_plots.pdf (visualization)")
print("  - CS17-G2FE_example_plots_Rotated_plots.pdf (visualization)")
