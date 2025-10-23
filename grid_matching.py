#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Regridding Dynamic Global Vegetation Model (DGVM) outputs to match 
the inversion grid resolution using bilinear interpolation.

This script:
1. Loads DGVM and inversion NetCDF datasets.
2. Examines their coordinate systems.
3. Constructs a regridding scheme to align DGVM data to the inversion grid.

Dependencies:
    - xarray
    - xesmf

Example:
    $ python regrid_dgvm_to_inv.py
"""

import xarray as xr
import xesmf as xe


def load_dataset(path: str) -> xr.Dataset:
    """Load a NetCDF dataset and display its dimensions and variables."""
    ds = xr.open_dataset(path)
    print(ds)
    print("Variables:", list(ds.data_vars))
    return ds


def prepare_target_grid(reference_ds: xr.Dataset, lat_name: str = "lat", lon_name: str = "lon") -> xr.Dataset:
    """Extract latitude and longitude from a reference dataset to define a target grid."""
    return xr.Dataset({
        "lat": reference_ds[lat_name],
        "lon": reference_ds[lon_name]
    })


def build_regridder(source_ds: xr.Dataset, target_ds: xr.Dataset, method: str = "bilinear", periodic: bool = True) -> xe.Regridder:
    """Create a regridder object for interpolating between grids."""
    return xe.Regridder(source_ds, target_ds, method=method, periodic=periodic)


def main():
    """Load data, prepare grids, and create a regridder."""
    # Load datasets
    dgvm_ds = load_dataset("data/dgvm/mean_grids.nc")
    inv_ds = load_dataset("data/inv/r76nbetEXToc_v2024E.flux.nc")

    # Standardize coordinate names
    dgvm_ds = dgvm_ds.rename({"latitude": "lat", "longitude": "lon"})

    # Define target grid
    target_grid = prepare_target_grid(inv_ds)

    # Build regridder
    regridder = build_regridder(dgvm_ds, target_grid)

    print("Regridder successfully created.")
    # Example usage:
    # regridded_var = regridder(dgvm_ds["your_variable_name"])


if __name__ == "__main__":
    main()
