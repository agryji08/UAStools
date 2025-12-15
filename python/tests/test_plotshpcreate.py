"""
Unit tests for plotshpcreate function.

Run with: pytest tests/
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from uastools import plotshpcreate


@pytest.fixture
def sample_data():
    """Create sample plot data for testing."""
    return pd.DataFrame({
        'Plot': [1, 1, 2, 2, 3, 3, 4, 4],
        'Range': [1, 1, 1, 1, 2, 2, 2, 2],
        'Row': [1, 2, 3, 4, 1, 2, 3, 4],
        'Barcode': [f'BC{i:03d}' for i in range(1, 9)]
    })


@pytest.fixture
def temp_dir():
    """Create temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        old_dir = os.getcwd()
        os.chdir(tmpdir)
        yield tmpdir
        os.chdir(old_dir)


def test_plotshpcreate_basic(sample_data, temp_dir):
    """Test basic shapefile creation."""
    plotshpcreate(
        A=(746239.817, 3382052.264),
        B=(746334.224, 3382152.870),
        UTMzone="14",
        Hemisphere="N",
        infile=sample_data,
        outfile="test_basic",
        field="TEST",
        SquarePlot=False,
        RotatePlot=False
    )

    # Check that shapefiles were created
    assert Path("TEST_test_basic.shp").exists()
    assert Path("TEST_test_basic_buff.shp").exists()


def test_plotshpcreate_missing_columns():
    """Test that missing required columns raises ValueError."""
    bad_data = pd.DataFrame({
        'Plot': [1, 2, 3],
        'Range': [1, 1, 1]
        # Missing 'Row' and 'Barcode'
    })

    with pytest.raises(ValueError, match="missing required columns"):
        plotshpcreate(
            A=(746239.817, 3382052.264),
            B=(746334.224, 3382152.870),
            infile=bad_data,
            outfile="test"
        )


def test_plotshpcreate_invalid_stagger(sample_data):
    """Test that invalid stagger parameter raises ValueError."""
    with pytest.raises(ValueError, match="Stagger must be in reference"):
        plotshpcreate(
            A=(746239.817, 3382052.264),
            B=(746334.224, 3382152.870),
            infile=sample_data,
            outfile="test",
            stagger=(1, 2, 0.5),  # Invalid: starts at 1
            SquarePlot=False,
            RotatePlot=False
        )


def test_plotshpcreate_multirow(sample_data, temp_dir):
    """Test multi-row plot creation."""
    plotshpcreate(
        A=(746239.817, 3382052.264),
        B=(746334.224, 3382152.870),
        UTMzone="14",
        Hemisphere="N",
        infile=sample_data,
        outfile="test_multirow",
        field="MULTI",
        nrowplot=2,
        multirowind=True,
        SquarePlot=False,
        RotatePlot=False
    )

    assert Path("MULTI_test_multirow.shp").exists()


def test_plotshpcreate_metric_units(sample_data, temp_dir):
    """Test shapefile creation with metric units."""
    plotshpcreate(
        A=(746239.817, 3382052.264),
        B=(746334.224, 3382152.870),
        UTMzone="14",
        Hemisphere="N",
        infile=sample_data,
        outfile="test_metric",
        field="METRIC",
        rowspc=0.76,
        rangespc=7.62,
        rowbuf=0.03,
        rangebuf=0.61,
        unit="meter",
        SquarePlot=False,
        RotatePlot=False
    )

    assert Path("METRIC_test_metric.shp").exists()


def test_plotshpcreate_southern_hemisphere(sample_data, temp_dir):
    """Test shapefile creation for Southern hemisphere."""
    plotshpcreate(
        A=(746239.817, -3382052.264),
        B=(746334.224, -3382152.870),
        UTMzone="14",
        Hemisphere="S",
        infile=sample_data,
        outfile="test_south",
        field="SOUTH",
        SquarePlot=False,
        RotatePlot=False
    )

    assert Path("SOUTH_test_south.shp").exists()


def test_plotshpcreate_no_utm(sample_data, temp_dir):
    """Test shapefile creation without UTM zone."""
    with pytest.warns(UserWarning, match="Coordinate reference system not defined"):
        plotshpcreate(
            A=(746239.817, 3382052.264),
            B=(746334.224, 3382152.870),
            UTMzone=None,
            infile=sample_data,
            outfile="test_no_utm",
            SquarePlot=False,
            RotatePlot=False
        )

    assert Path("test_no_utm.shp").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
