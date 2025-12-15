# UAStools 0.5.0

## Major Changes

* **CRAN Compatibility Update**: Package has been updated to comply with current CRAN requirements
* **Migration from rgdal/sp to sf**: All spatial operations now use the modern `sf` package
  - `rgdal` package was retired from CRAN in October 2023
  - `sp` package dependencies replaced with `sf` equivalents
  - All shapefile reading/writing now uses `sf::st_write()` instead of `rgdal::writeOGR()`
  - Coordinate reference system handling now uses `sf::st_crs()` instead of `sp::CRS()`

## Package Metadata Updates

* Updated DESCRIPTION file to use `Authors@R` field per CRAN standards
* Fixed Description field to not start with "This package"
* Updated Date field to ISO 8601 format (YYYY-MM-DD)
* Version bumped to 0.5.0 to reflect major dependency changes

## Documentation Improvements

* Fixed examples to comply with CRAN policies:
  - Wrapped examples in `\dontrun{}` to prevent modification of user workspace
  - Changed to use `tempdir()` instead of hardcoded paths
  - Fixed syntax errors in example code (missing comma)
* Updated NAMESPACE to reflect new dependencies

## Breaking Changes

* **Users must now install the `sf` package** instead of `rgdal` and `sp`
* The output shapefiles are functionally identical, but generated using modern spatial infrastructure
* All existing scripts should continue to work without modification

## Notes

This update ensures the package remains compatible with current R spatial ecosystem and meets CRAN submission requirements. The `sf` package is actively maintained and provides better performance and more features than the retired `rgdal` package.

# UAStools 0.4.0

Previous version using rgdal/sp packages.
