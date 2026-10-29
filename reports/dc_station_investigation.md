# Independent Investigation of DC Precipitation Stations

## 1. Objective

Investigate publicly available precipitation observations from stations physically located within Washington, DC, independently of the MRMS gridded precipitation dataset.

## 2. Search Strategy

The NOAA NCEI Daily Summaries search API was queried using a geographic bounding box covering Washington, DC.

Search parameters:
- Dataset: daily-summaries
- Bounding box: 39.00, -77.12, 38.79, -76.90
- Initial search period: 2021
- Variable of interest: PRCP (precipitation)

Five candidate stations with identifiers beginning with US1DCDC were identified.

Their coordinates and reporting histories were examined. Two stations were selected for further data retrieval and integration.

## 3. Selected Stations

| Station ID | Name | Latitude | Longitude |
|---|---|---:|---:|
| US1DCDC0014 | Washington 5.1 NW, DC US | 38.958091 | -77.081730 |
| US1DCDC0026 | Washington 2.6 NE, DC US | 38.932715 | -76.983545 |

Both stations are located in Washington, DC, based on their reported locations.

Washington Reagan National Airport (USW00013743) was also returned during the geographic search, but it is located in Virginia and was not treated as an in-DC station.

### Verification Against the Official DC Boundary

The reported NOAA station coordinates were checked against
the official DC GIS administrative boundary (Layer 10:
DC Boundary), using an ArcGIS point-intersection query
with EPSG:4326 coordinates.

Results:
- US1DCDC0014: inside DC (1 boundary match)
- US1DCDC0026: inside DC (1 boundary match)

Official GIS service:
https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Administrative_Other_Boundaries/MapServer/10

This confirms that both reported station coordinates fall
within the official Washington, DC boundary. Washington
Reagan National Airport, located in Virginia, was not
classified as an in-DC precipitation station.

## 4. Data Access

Daily precipitation records were retrieved using the NOAA NCEI Data Access API:

https://www.ncei.noaa.gov/access/services/data/v1

Parameters:
- Dataset: daily-summaries
- Variable: PRCP
- Units: metric
- Format: CSV
- Include attributes: true

The retrieval period was 2015–2025.

Downloaded files:
- data/raw/stations/US1DCDC0014_daily.csv
- data/raw/stations/US1DCDC0026_daily.csv

## 5. Data Availability

US1DCDC0014:
- 3,255 reported records
- 3,225 valid precipitation values
- 30 records with missing PRCP
- Coverage: 80.26% over the observed date span

US1DCDC0026:
- 1,834 reported records
- 1,771 valid precipitation values
- 63 records with missing PRCP
- Coverage: 69.13% over the observed date span

Coverage percentages account for dates without records as well as records with missing precipitation values.

Annual coverage is documented in:
reports/dc_station_coverage.csv

Flood-event date coverage is documented in:
reports/dc_station_event_coverage.csv

## 6. Integration into HDF5

The precipitation observations were stored under:

stations/precipitation/<station_id>/

Each station group contains:
- date
- precipitation
- quality_attributes

Station coordinates, units, source information, temporal resolution, and missing-value conventions are stored as HDF5 attributes.

## 7. Limitations

- Observations are daily totals, not hourly measurements.
- Exact daily observation cutoff times were not verified.
- Missing values and absent dates are distinct from zero precipitation.
- Coverage is incomplete and varies substantially across years.
- Daily station records cannot be assumed to coincide exactly with flood-event time windows.
- Differences between stations may reflect spatial rainfall variability.

## 8. Reproducibility

Station discovery:
python src/find_dc_stations.py

Historical data retrieval:
python src/download_station_history.py

HDF5 integration:
python src/add_dc_stations_hdf5.py

Coverage assessment:
python src/station_coverage.py
python src/station_event_coverage.py
