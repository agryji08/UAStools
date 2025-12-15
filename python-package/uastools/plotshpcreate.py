"""
Plot Shapefile Creation Module

Methods for constructing multipolygon ESRI shapefiles (.shp) with individual
polygons containing agricultural plot boundaries. Utilizes AB line to rotate
polygons to the appropriate geospatial direction of research plots.
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Tuple, Union
import warnings


def plotshpcreate(
    A: Tuple[float, float],
    B: Tuple[float, float],
    infile: pd.DataFrame,
    outfile: str,
    UTMzone: Optional[str] = None,
    Hemisphere: str = "N",
    nrowplot: int = 1,
    multirowind: bool = False,
    rowspc: float = 2.5,
    rowbuf: float = 0.1,
    rangespc: float = 25.0,
    rangebuf: float = 2.0,
    stagger: Optional[Tuple[int, int, float]] = None,
    plotsubset: int = 0,
    field: Optional[str] = None,
    unit: str = "feet",
    SquarePlot: bool = True,
    RotatePlot: bool = True
) -> None:
    """
    Create plot shapefiles for agricultural field trials.

    Parameters
    ----------
    A : tuple of (float, float)
        Vector of UTM coordinates (Easting, Northing) of "A" point, which corresponds
        to the bottom left corner of the first field plot.
    B : tuple of (float, float)
        Vector of UTM coordinates (Easting, Northing) of "B" point, which corresponds
        to the top left corner of the field trial within the same row as the "A" point.
    infile : pd.DataFrame
        DataFrame containing seed preparation file and experimental design
        (i.e., coordinates of plots within the design grid). Must contain columns:
        'Plot', 'Range', 'Row', and 'Barcode'.
    outfile : str
        Output file name prefix (without .shp extension).
    UTMzone : str, optional
        UTM zone number. Default is None and will result in a coordinate reference
        system of "NA".
    Hemisphere : str, default "N"
        Designates the Northern "N" or Southern "S" Hemisphere.
    nrowplot : int, default 1
        Number of adjacent rows that constitute a plot.
    multirowind : bool, default False
        If True, adjacent plot rows should be treated as separate plots with unique
        identifiers. If False, combines adjacent plots into a single polygon.
    rowspc : float, default 2.5
        Row (i.e., column) spacing of a single row in feet or meters.
        Default 2.5 feet (30 inch row spacing).
    rowbuf : float, default 0.1
        Distance removed from both sides of rowspc to create a buffer zone.
    rangespc : float, default 25
        Range (i.e., row) spacing of a single row.
    rangebuf : float, default 2
        Distance removed from both sides of rangespc to create a buffer zone.
    stagger : tuple of (int, int, float), optional
        Defines [1] row where stagger starts, [2] rows sowed in a single pass,
        and [3] stagger offset distance from A point.
    plotsubset : int, default 0
        Defines how many adjacent rows should be excluded from the shapefile.
    field : str, optional
        Field trial identifier (e.g., "CS17-G2FE").
    unit : str, default "feet"
        Unit of measure for polygon dimensions. Can be "feet" or "meter".
    SquarePlot : bool, default True
        If True, create PDF file for visualization of non-rotated polygons.
    RotatePlot : bool, default True
        If True, create PDF file for visualization of rotated polygons.

    Returns
    -------
    None
        Function creates shapefiles and optional PDF visualizations as side effects.

    Examples
    --------
    >>> import pandas as pd
    >>> # Create sample data
    >>> infile = pd.DataFrame({
    ...     'Plot': range(1, 101),
    ...     'Range': [i//10 + 1 for i in range(100)],
    ...     'Row': [i%10 + 1 for i in range(100)],
    ...     'Barcode': [f'BC{i:03d}' for i in range(1, 101)]
    ... })
    >>>
    >>> plotshpcreate(
    ...     A=(746239.817, 3382052.264),
    ...     B=(746334.224, 3382152.870),
    ...     UTMzone="14",
    ...     Hemisphere="N",
    ...     infile=infile,
    ...     outfile="test_plots",
    ...     field="CS17-G2FE"
    ... )
    """
    # Validate inputs
    if not isinstance(infile, pd.DataFrame):
        raise TypeError("infile must be a pandas DataFrame")

    required_cols = ['Plot', 'Range', 'Row', 'Barcode']
    missing_cols = [col for col in required_cols if col not in infile.columns]
    if missing_cols:
        raise ValueError(f"infile missing required columns: {missing_cols}")

    # Validate stagger parameter
    if stagger is not None:
        if stagger[0] == 1:
            raise ValueError("Stagger must be in reference to plots beyond first plot polygon, i.e. stagger[0] != 1")
        if stagger[0] > (stagger[1] + 1):
            raise ValueError("Stagger is based on planter dimensions and was built for consistent stagger throughout the trial")
        if nrowplot > 1 and not multirowind and (nrowplot > (stagger[1] / 2)):
            raise ValueError("Combined plots will not be correctly adjusted by stagger. Recommend setting multirowind=True")

    # Set precision
    np.set_printoptions(precision=12)

    # Order infile by plot numbers numerically, then by row number
    infile = infile.sort_values(['Plot', 'Row'], key=lambda x: pd.to_numeric(x, errors='coerce'))
    infile = infile.reset_index(drop=True)

    nRange = len(infile['Range'].unique())
    nRow = len(infile['Row'].unique())
    nPlot = len(infile)

    if nPlot != (nRange * nRow):
        warnings.warn("Length of file is not equal to number of plots: may cause errors")

    # Calculate AB line deltas and theta
    DeltaEasting = B[0] - A[0]
    DeltaNorthing = B[1] - A[1]
    DirectionTheta = np.arctan(abs(DeltaNorthing) / abs(DeltaEasting))

    # Determine quadrant and calculate rotation angle
    if DeltaNorthing > 0 and DeltaEasting > 0:  # Quadrant I
        Theta = ((3 * np.pi) / 2) + DirectionTheta
        srt_theta = 90 - DirectionTheta * (180 / np.pi)
    elif DeltaNorthing > 0 and DeltaEasting < 0:  # Quadrant II
        Theta = ((np.pi) / 2) - DirectionTheta
        srt_theta = 270 + DirectionTheta * (180 / np.pi)
    elif DeltaNorthing < 0 and DeltaEasting < 0:  # Quadrant III
        Theta = ((np.pi) / 2) + DirectionTheta
        srt_theta = DirectionTheta * (180 / np.pi)
    else:  # Quadrant IV
        Theta = ((3 * np.pi) / 2) - DirectionTheta
        srt_theta = 270 + DirectionTheta * (180 / np.pi)

    # Convert units to meters
    if unit == "feet":
        RangeSpacingM = rangespc / 3.281
        RowSpacingM = rowspc / 3.281
        RangeBufferM = rangebuf / 3.281
        RowBufferM = rowbuf / 3.281
        staggerM = stagger[2] / 3.281 if stagger else None
    else:  # meter
        RangeSpacingM = rangespc
        RowSpacingM = rowspc
        RangeBufferM = rangebuf
        RowBufferM = rowbuf
        staggerM = stagger[2] if stagger else None

    # Create plot matrix
    PlotsSquareM = np.zeros((nPlot, 12))
    PlotsSquareM[:, 0] = infile['Plot'].values
    PlotsSquareM[:, 1] = infile['Range'].values - infile['Range'].min() + 1  # RANGE = Y
    PlotsSquareM[:, 2] = infile['Row'].values - infile['Row'].min() + 1  # ROW = X
    PlotsSquareM[:, 11] = PlotsSquareM[:, 2].copy()  # Keep original row numbering

    # Create row names (IDs) from barcodes
    row_names = infile['Barcode'].astype(str).tolist()

    # Handle multi-row plots
    if nrowplot > 1 and not multirowind and plotsubset == 0:
        # Adjust spacing for combined rows
        if unit == "feet":
            RowSpacingM = (nrowplot * rowspc) / 3.281
        else:
            RowSpacingM = nrowplot * rowspc

        # Create unique IDs and filter rows
        unique_barcodes = infile['Barcode'].unique()
        mask = (PlotsSquareM[:, 2] == (1 + plotsubset)) | np.isin(
            PlotsSquareM[:, 2],
            np.arange(1 + nrowplot + plotsubset, PlotsSquareM[:, 2].max() + 1, nrowplot)
        )

        PlotsSquareM = PlotsSquareM[mask]
        row_names = [row_names[i] for i, m in enumerate(mask) if m]

        # Adjust row numbers
        for i in range(len(PlotsSquareM)):
            if PlotsSquareM[i, 2] > 1:
                PlotsSquareM[i, 2] = np.ceil(PlotsSquareM[i, 2] / nrowplot)

    # Handle multi-row with individual IDs or plotsubset
    if (nrowplot > 1 and multirowind) or (plotsubset != 0):
        unique_barcodes = infile['Barcode'].unique()
        new_row_names = []

        for barcode in unique_barcodes:
            subset_indices = np.where(infile['Barcode'] == barcode)[0]
            subset_rows = PlotsSquareM[subset_indices, 2]

            for k, idx in enumerate(subset_indices):
                new_row_names.append(f"{barcode}_{k+1}")

        row_names = new_row_names[:len(PlotsSquareM)]

        # Handle plotsubset
        if plotsubset != 0:
            if nrowplot == 1:
                raise ValueError("nrowplot == 1: Cannot subset singular plot")
            if nrowplot < 3:
                raise ValueError("nrowplot < 3: Cannot subset central plot. Recommend nrowplot=2, multirowind=True, plotsubset=0")
            if nrowplot == 2 * plotsubset:
                raise ValueError("nrowplot == 2*plotsubset: no polygons will be created")

            # Create mask for interior plots
            plot_mask = np.zeros(len(PlotsSquareM), dtype=bool)
            for i in range(len(PlotsSquareM)):
                plot_num = PlotsSquareM[i, 0]
                plot_rows = PlotsSquareM[PlotsSquareM[:, 0] == plot_num, 2]
                plot_mask[i] = PlotsSquareM[i, 2] in np.arange(
                    plot_rows.min() + plotsubset,
                    plot_rows.max() - plotsubset + 1
                )

            PlotsSquareM = PlotsSquareM[plot_mask]
            row_names = [row_names[i] for i, m in enumerate(plot_mask) if m]

    # Serpentine ordering
    ordered_plots = []
    ordered_names = []
    for i in range(1, nRange + 1):
        range_mask = PlotsSquareM[:, 1] == i
        subset_PSM = PlotsSquareM[range_mask]
        subset_names = [row_names[j] for j, m in enumerate(range_mask) if m]

        # Sort by row
        sort_idx = np.argsort(subset_PSM[:, 2])
        if i % 2 == 0:  # Reverse every other range
            sort_idx = sort_idx[::-1]

        ordered_plots.append(subset_PSM[sort_idx])
        ordered_names.extend([subset_names[j] for j in sort_idx])

    PlotsSquareM = np.vstack(ordered_plots)
    row_names = ordered_names
    PlotSquare4plot = PlotsSquareM.copy()

    # Calculate corner coordinates (non-rotated)
    ZeroZero = np.array([0.0, 0.0])

    for i in range(len(PlotsSquareM)):
        # Bottom left
        PlotsSquareM[i, 3] = ZeroZero[0] + ((PlotsSquareM[i, 1] - 1) * RangeSpacingM)
        PlotsSquareM[i, 4] = ZeroZero[1] + ((PlotsSquareM[i, 2] - 1) * RowSpacingM)
        # Bottom right
        PlotsSquareM[i, 5] = ZeroZero[0] + ((PlotsSquareM[i, 1] - 1) * RangeSpacingM)
        PlotsSquareM[i, 6] = ZeroZero[1] + (PlotsSquareM[i, 2] * RowSpacingM)
        # Top right
        PlotsSquareM[i, 7] = ZeroZero[0] + (PlotsSquareM[i, 1] * RangeSpacingM)
        PlotsSquareM[i, 8] = ZeroZero[1] + (PlotsSquareM[i, 2] * RowSpacingM)
        # Top left
        PlotsSquareM[i, 9] = ZeroZero[0] + (PlotsSquareM[i, 1] * RangeSpacingM)
        PlotsSquareM[i, 10] = ZeroZero[1] + ((PlotsSquareM[i, 2] - 1) * RowSpacingM)

    # Apply stagger if specified
    if stagger is not None:
        PlotSquare4plot = PlotsSquareM.copy()
        for i in range(len(PlotsSquareM)):
            stagger_check = np.ceil((np.floor((PlotsSquareM[i, 11] - stagger[0]) + 1) + stagger[1]) / stagger[1]) % 2
            if stagger_check == 0:
                PlotSquare4plot[i, 3] += staggerM
                PlotSquare4plot[i, 5] += staggerM
                PlotSquare4plot[i, 7] += staggerM
                PlotSquare4plot[i, 9] += staggerM

    # Create buffered version
    PlotsSquareMBuf = PlotsSquareM.copy()

    for i in range(len(PlotsSquareMBuf)):
        # Bottom left
        PlotsSquareMBuf[i, 3] += RangeBufferM
        PlotsSquareMBuf[i, 4] += RowBufferM
        # Bottom right
        PlotsSquareMBuf[i, 5] += RangeBufferM
        PlotsSquareMBuf[i, 6] -= RowBufferM
        # Top right
        PlotsSquareMBuf[i, 7] -= RangeBufferM
        PlotsSquareMBuf[i, 8] -= RowBufferM
        # Top left
        PlotsSquareMBuf[i, 9] -= RangeBufferM
        PlotsSquareMBuf[i, 10] += RowBufferM

    # Create square plot visualization if requested
    if SquarePlot:
        _create_square_plot(PlotSquare4plot, PlotsSquareMBuf, row_names,
                           field, outfile, nRow, nRange, RowSpacingM, RangeSpacingM)

    # Rotate plots based on AB line
    EastingCorner_0_0 = A[0]
    NorthingCorner_0_0 = A[1]

    # Calculate staggered origin if needed
    if stagger is not None:
        if DeltaNorthing > 0 and DeltaEasting > 0:  # Quadrant I
            EastingCorner_0_0_stag = EastingCorner_0_0 - staggerM * np.sin(Theta)
            NorthingCorner_0_0_stag = NorthingCorner_0_0 + staggerM * np.cos(Theta)
        elif DeltaNorthing > 0 and DeltaEasting < 0:  # Quadrant II
            EastingCorner_0_0_stag = EastingCorner_0_0 - staggerM * np.cos(Theta)
            NorthingCorner_0_0_stag = NorthingCorner_0_0 + staggerM * np.sin(Theta)
        elif DeltaNorthing < 0 and DeltaEasting < 0:  # Quadrant III
            EastingCorner_0_0_stag = EastingCorner_0_0 - staggerM * np.cos(Theta)
            NorthingCorner_0_0_stag = NorthingCorner_0_0 + staggerM * np.sin(Theta)
        else:  # Quadrant IV
            EastingCorner_0_0_stag = EastingCorner_0_0 + staggerM * np.cos(Theta)
            NorthingCorner_0_0_stag = NorthingCorner_0_0 - staggerM * np.sin(Theta)

    PlotsAdjustedM = PlotsSquareM.copy()
    PlotsAdjustedMBuf = PlotsSquareMBuf.copy()

    # Apply rotation
    for i in range(len(PlotsAdjustedM)):
        use_stagger = False
        if stagger is not None:
            stagger_check = np.ceil((np.floor((PlotsSquareM[i, 11] - stagger[0]) + 1) + stagger[1]) / stagger[1]) % 2
            use_stagger = (stagger_check == 0)

        origin_E = EastingCorner_0_0_stag if use_stagger else EastingCorner_0_0
        origin_N = NorthingCorner_0_0_stag if use_stagger else NorthingCorner_0_0

        # Rotate each corner (columns 3-10 contain Y,X pairs)
        for j in range(4):
            y_idx = 3 + j * 2
            x_idx = 4 + j * 2

            # Rotate coordinates
            PlotsAdjustedM[i, y_idx] = (PlotsSquareM[i, y_idx] * np.cos(Theta) +
                                        PlotsSquareM[i, x_idx] * np.sin(Theta) + origin_N)
            PlotsAdjustedM[i, x_idx] = (PlotsSquareM[i, x_idx] * np.cos(Theta) -
                                        PlotsSquareM[i, y_idx] * np.sin(Theta) + origin_E)

            # Rotate buffered coordinates
            PlotsAdjustedMBuf[i, y_idx] = (PlotsSquareMBuf[i, y_idx] * np.cos(Theta) +
                                           PlotsSquareMBuf[i, x_idx] * np.sin(Theta) + origin_N)
            PlotsAdjustedMBuf[i, x_idx] = (PlotsSquareMBuf[i, x_idx] * np.cos(Theta) -
                                           PlotsSquareMBuf[i, y_idx] * np.sin(Theta) + origin_E)

    # Create rotated plot visualization if requested
    if RotatePlot:
        _create_rotated_plot(PlotsAdjustedM, PlotsAdjustedMBuf, row_names,
                            field, outfile, srt_theta)

    # Set CRS
    if UTMzone is None:
        crs = None
        warnings.warn("Coordinate reference system not defined 'UTMzone=None'; "
                     "This may result in difficulties loading shapefiles into other programs.")
    else:
        if Hemisphere == "N":
            crs = f"+proj=utm +zone={UTMzone} +datum=NAD83 +units=m +no_defs +ellps=GRS80"
        else:
            crs = f"+proj=utm +zone={UTMzone} +south +datum=NAD83 +units=m +no_defs +ellps=GRS80"

    # Create shapefiles
    _write_shapefile(PlotsAdjustedM, row_names, field, outfile, crs, buffered=False)
    _write_shapefile(PlotsAdjustedMBuf, row_names, field, outfile, crs, buffered=True)


def _create_square_plot(PlotsSquareM, PlotsSquareMBuf, row_names, field, outfile,
                        nRow, nRange, RowSpacingM, RangeSpacingM):
    """Create visualization of non-rotated plots."""
    fig, ax = plt.subplots(figsize=(15, 15))

    max_row = PlotsSquareM[:, 2].max()
    ax.set_xlim(0, max_row * RowSpacingM)
    ax.set_ylim(0, nRange * RangeSpacingM)
    ax.set_xlabel('ROWS (meters)')
    ax.set_ylabel('RANGES (meters)')

    for i in range(len(PlotsSquareM)):
        # Plot coordinates
        plot_x = [PlotsSquareM[i, 4], PlotsSquareM[i, 6], PlotsSquareM[i, 8], PlotsSquareM[i, 10], PlotsSquareM[i, 4]]
        plot_y = [PlotsSquareM[i, 3], PlotsSquareM[i, 5], PlotsSquareM[i, 7], PlotsSquareM[i, 9], PlotsSquareM[i, 3]]

        # Buffered coordinates
        buf_x = [PlotsSquareMBuf[i, 4], PlotsSquareMBuf[i, 6], PlotsSquareMBuf[i, 8], PlotsSquareMBuf[i, 10], PlotsSquareMBuf[i, 4]]
        buf_y = [PlotsSquareMBuf[i, 3], PlotsSquareMBuf[i, 5], PlotsSquareMBuf[i, 7], PlotsSquareMBuf[i, 9], PlotsSquareMBuf[i, 3]]

        ax.plot(plot_x, plot_y, 'k-')
        ax.fill(buf_x, buf_y, 'red', alpha=0.5)

        # Add plot number
        center_x = (buf_x[0] + buf_x[2]) / 2
        center_y = (buf_y[0] + buf_y[2]) / 2
        ax.text(center_x, center_y, str(int(PlotsSquareM[i, 0])),
               ha='center', va='center', color='white', fontsize=7)

    filename = f"{field}_{outfile}_Square_plots.pdf" if field else f"{outfile}_Square_plots.pdf"
    plt.savefig(filename, format='pdf')
    plt.close()


def _create_rotated_plot(PlotsAdjustedM, PlotsAdjustedMBuf, row_names,
                        field, outfile, srt_theta):
    """Create visualization of rotated plots."""
    fig, ax = plt.subplots(figsize=(30, 30))

    # Get all X and Y coordinates
    all_x = PlotsAdjustedM[:, [4, 6, 8, 10]].flatten()
    all_y = PlotsAdjustedM[:, [3, 5, 7, 9]].flatten()

    ax.set_xlim(all_x.min(), all_x.max())
    ax.set_ylim(all_y.min(), all_y.max())
    ax.set_xlabel('UTM Easting Coordinates (m)')
    ax.set_ylabel('UTM Northing Coordinates (m)')

    for i in range(len(PlotsAdjustedM)):
        # Plot coordinates
        plot_x = [PlotsAdjustedM[i, 4], PlotsAdjustedM[i, 6], PlotsAdjustedM[i, 8], PlotsAdjustedM[i, 10], PlotsAdjustedM[i, 4]]
        plot_y = [PlotsAdjustedM[i, 3], PlotsAdjustedM[i, 5], PlotsAdjustedM[i, 7], PlotsAdjustedM[i, 9], PlotsAdjustedM[i, 3]]

        # Buffered coordinates
        buf_x = [PlotsAdjustedMBuf[i, 4], PlotsAdjustedMBuf[i, 6], PlotsAdjustedMBuf[i, 8], PlotsAdjustedMBuf[i, 10], PlotsAdjustedMBuf[i, 4]]
        buf_y = [PlotsAdjustedMBuf[i, 3], PlotsAdjustedMBuf[i, 5], PlotsAdjustedMBuf[i, 7], PlotsAdjustedMBuf[i, 9], PlotsAdjustedMBuf[i, 3]]

        ax.plot(plot_x, plot_y, 'k-')
        ax.fill(buf_x, buf_y, 'red', alpha=0.5)

        # Add plot number
        center_x = (plot_x[0] + plot_x[2]) / 2
        center_y = (plot_y[0] + plot_y[2]) / 2
        ax.text(center_x, center_y, str(int(PlotsAdjustedM[i, 0])),
               ha='center', va='center', color='blue', fontsize=7,
               rotation=srt_theta)

    filename = f"{field}_{outfile}_Rotated_plots.pdf" if field else f"{outfile}_Rotated_plots.pdf"
    plt.savefig(filename, format='pdf')
    plt.close()


def _write_shapefile(PlotsAdjusted, row_names, field, outfile, crs, buffered=False):
    """Write plots to shapefile using geopandas."""
    polygons = []

    for i in range(len(PlotsAdjusted)):
        # Extract coordinates (X, Y order for shapely)
        coords = [
            (PlotsAdjusted[i, 4], PlotsAdjusted[i, 3]),  # Bottom left
            (PlotsAdjusted[i, 6], PlotsAdjusted[i, 5]),  # Bottom right
            (PlotsAdjusted[i, 8], PlotsAdjusted[i, 7]),  # Top right
            (PlotsAdjusted[i, 10], PlotsAdjusted[i, 9]), # Top left
            (PlotsAdjusted[i, 4], PlotsAdjusted[i, 3]),  # Close polygon
        ]
        polygons.append(Polygon(coords))

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {'id': row_names},
        geometry=polygons,
        crs=crs
    )

    # Determine output filename
    if buffered:
        filename = f"{field}_{outfile}_buff.shp" if field else f"{outfile}_buff.shp"
    else:
        filename = f"{field}_{outfile}.shp" if field else f"{outfile}.shp"

    # Write to shapefile
    gdf.to_file(filename, driver='ESRI Shapefile')
    print(f"Shapefile written to: {filename}")
