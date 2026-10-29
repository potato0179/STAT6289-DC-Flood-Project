# Reproducible Environmental Database for DC Flood Events

STAT 6289 — Washington, DC Flood Data Project

## 1. Project Overview

This project builds a reproducible HDF5 environmental database for 125 reported flood events in Washington, DC, covering 1996–2025.

Assigned dataset version: Version 5 — NOAA MRMS gridded precipitation and DC precipitation stations.

The database integrates flood event timestamps, hourly gridded precipitation, and daily station observations.

## 2. Data Sources

### Flood Events
- Input: `data/raw/DC_flood_times.csv`
- 125 reported flood events
- Original timestamps interpreted as fixed EST (UTC-5), including summer dates
- UTC timestamps stored in the database

### NOAA MRMS
- Product: `MultiSensor_QPE_01H_Pass2`
- Variable: one-hour precipitation accumulation
- Units: mm
- Spatial resolution: approximately 0.01 degrees
- DC spatial subset: 38.7–39.1°N, 77.3–76.8°W
- Raster shape: 40 × 50
- Temporal metadata: UTC, with timestamps marking the end of each accumulation interval

126 hourly rasters were obtained from the selected public archive.

Archive coverage is incomplete, especially for older events. Missing archive files are never interpreted as zero precipitation.

### DC Precipitation Stations
Source: NOAA NCEI GHCN-Daily, accessed through the daily-summaries API.

| Station ID | Station Name | Latitude | Longitude |
|---|---|---:|---:|
| US1DCDC0014 | Washington 5.1 NW | 38.958091 | -77.081730 |
| US1DCDC0026 | Washington 2.6 NE | 38.932715 | -76.983545 |

- Variable: PRCP
- Units: mm
- Temporal resolution: daily
- Stored records: 5,089
- Missing values are preserved as NaN
- Original precipitation attributes are retained

The exact daily observation cutoff times have not been verified. Daily station precipitation must not be interpreted as exact hourly flood-event rainfall.

### Independent DC Station Investigation

An independent investigation of precipitation stations within
Washington, DC, was conducted using NOAA NCEI station records.

The search strategy, candidate stations, geographic locations,
data availability, access methods, and limitations are documented in:

[DC Station Investigation Report](reports/dc_station_investigation.md)

## 3. HDF5 Database Structure

Database: `data/processed/dc_flood_database.h5`

```text
/
├── events/
│   ├── event_001/
│   └── ...
├── gridded/
│   └── mrms/
│       ├── YYYY-MM-DD_HHMM/
│       │   ├── precipitation
│       │   ├── latitude
│       │   └── longitude
│       └── ...
└── stations/
    └── precipitation/
        ├── US1DCDC0014/
        └── US1DCDC0026/
            ├── date
            ├── precipitation
            └── quality_attributes
```

The database stores source, units, spatial coordinates, and temporal metadata.

## 4. Installation

Python dependencies are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

GRIB2 decoding requires the cfgrib/ecCodes software stack.

## 5. Reproducing the Database

Run commands from the project root.

### Flood event preparation

```bash
python src/check_events.py
python src/create_hdf5.py
python src/add_events.py
```

`create_hdf5.py` initializes a database only if it does not already exist.

### MRMS acquisition and integration

```bash
python src/plan_mrms_downloads.py
python src/filter_mrms_plan.py
```

MRMS download availability was checked separately. The available-file queue is stored in:

`data/processed/mrms_download_queue.csv`

Download the available MRMS files listed in the saved queue:

```bash
python src/download_mrms.py
```

Then integrate the downloaded files into HDF5:

```bash
python src/batch_mrms_to_hdf5.py
python src/event_coverage.py
```

Raw MRMS downloads are excluded from Git because of file size. The processed HDF5 database is included in the repository.

### Station data preparation

```bash
python src/download_station_history.py
python src/add_dc_stations_hdf5.py
python src/station_coverage.py
python src/station_event_coverage.py
python src/generate_quality_report.py
```

## 6. Reading and Visualizing HDF5 Data

Read DC station precipitation directly from HDF5:

```bash
python src/read_station_timeseries.py
```

Generate the station rainfall visualization:

```bash
python src/plot_station_rainfall.py
```

MRMS visualization:

```bash
python src/plot_event_rainfall.py
```

Generated figures are stored in `figures/`.

### Reusable HDF5 Data Access

List available database contents:

```bash
python src/list_hdf5_contents.py
```

Retrieve MRMS rasters for a selected flood event:

```python
from src.read_mrms_event import get_event_rasters

rasters = get_event_rasters("event_125")

selected = get_event_rasters(
    "event_125",
    "2025-07-19T23:00:00Z"
)
```

Retrieve daily station precipitation:

```python
from src.read_station_timeseries import get_station_timeseries

daily = get_station_timeseries(
    "US1DCDC0014",
    "2021-09-15",
    "2021-09-18"
)
```

These functions read the processed HDF5 database directly.
Station dates are source-reported observation dates,
not verified hourly event intervals.

## 7. Data Coverage and Limitations

MRMS event coverage:
- Complete: 26 events
- Partial: 1 event
- Missing: 98 events

DC station event-date coverage:
- US1DCDC0014: 43 complete, 0 partial, 82 missing
- US1DCDC0026: 22 complete, 1 partial, 102 missing

The station coverage classification indicates availability on the source-reported dates. It does not guarantee observations for the exact flood-event hours.

Additional limitations:
- Historical MRMS archive availability is incomplete.
- Station daily accumulation boundaries remain unverified.
- Missing observations are distinct from measured zero rainfall.
- Spatial variation between observation stations is expected.
- Daily station totals cannot be directly equated with hourly MRMS totals.

See `reports/data_quality_report.md` and `reports/mrms_availability_summary.md` for detailed coverage documentation.

## 8. Reproducibility Notes

The repository contains:
- Original flood event timestamps
- Python source code
- Processed HDF5 database
- Data quality reports
- Reproducible visualization scripts

The MRMS download queue records files found at the selected archive when the availability assessment was performed. A fresh reconstruction from online sources may return different file availability.

## 9. AI Assistance Disclosure

OpenAI ChatGPT was used to assist with workflow planning, Python code development, debugging, HDF5 database organization, data validation, and documentation.
