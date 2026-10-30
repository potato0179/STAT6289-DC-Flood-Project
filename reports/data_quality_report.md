# DC Flood Database — Data Quality Report

## 1. MRMS Gridded Precipitation

Source: NOAA MRMS MultiSensor_QPE_01H_Pass2

Event coverage:

- missing: 97 events
- complete: 26 events
- zero_duration: 1 event
- partial: 1 event

Missing MRMS archive files are not interpreted as zero rainfall.

## 2. DC Precipitation Stations

Source: NOAA NCEI daily-summaries (PRCP)
Units: mm
Temporal resolution: daily

Event-date coverage:

- US1DCDC0014: 43 complete, 0 partial, 82 missing
- US1DCDC0026: 22 complete, 1 partial, 102 missing

## 3. Annual Station Coverage

| Station | Year | Valid days | Expected days | Coverage |
|---|---:|---:|---:|---:|
| US1DCDC0014 | 2015 | 306 | 365 | 83.8% |
| US1DCDC0014 | 2016 | 327 | 366 | 89.3% |
| US1DCDC0014 | 2017 | 340 | 365 | 93.2% |
| US1DCDC0014 | 2018 | 10 | 365 | 2.7% |
| US1DCDC0014 | 2019 | 122 | 365 | 33.4% |
| US1DCDC0014 | 2020 | 362 | 366 | 98.9% |
| US1DCDC0014 | 2021 | 354 | 365 | 97.0% |
| US1DCDC0014 | 2022 | 346 | 365 | 94.8% |
| US1DCDC0014 | 2023 | 331 | 365 | 90.7% |
| US1DCDC0014 | 2024 | 366 | 366 | 100.0% |
| US1DCDC0014 | 2025 | 361 | 365 | 98.9% |
| US1DCDC0026 | 2018 | 1 | 5 | 20.0% |
| US1DCDC0026 | 2019 | 1 | 365 | 0.3% |
| US1DCDC0026 | 2020 | 76 | 366 | 20.8% |
| US1DCDC0026 | 2021 | 321 | 365 | 87.9% |
| US1DCDC0026 | 2022 | 329 | 365 | 90.1% |
| US1DCDC0026 | 2023 | 343 | 365 | 94.0% |
| US1DCDC0026 | 2024 | 360 | 366 | 98.4% |
| US1DCDC0026 | 2025 | 340 | 365 | 93.2% |

## 4. Important Limitations

- Station observation cutoff times have not been verified.
- Station daily totals cannot be treated as exact hourly event rainfall.
- Missing observations and zero precipitation are distinct.
- Station coverage varies substantially across years.
- MRMS archive availability is incomplete for historical events.

## 5. Reproducibility

The processed data are stored in `data/processed/dc_flood_database.h5`.

Analysis scripts read the HDF5 database directly.
