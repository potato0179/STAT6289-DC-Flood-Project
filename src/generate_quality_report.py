
import pandas as pd
from pathlib import Path

mrms = pd.read_csv("reports/mrms_event_coverage.csv")
stations = pd.read_csv("reports/dc_station_event_coverage.csv")
station_daily = pd.read_csv("reports/dc_station_coverage.csv")

lines = [
    "# DC Flood Database — Data Quality Report",
    "",
    "## 1. MRMS Gridded Precipitation",
    "",
    "Source: NOAA MRMS MultiSensor_QPE_01H_Pass2",
    "",
    "Event coverage:",
    ""
]

for status, count in mrms["status"].value_counts().items():
    lines.append(f"- {status}: {count} events")

lines.extend([
    "",
    "Missing MRMS archive files are not interpreted as zero rainfall.",
    "",
    "## 2. DC Precipitation Stations",
    "",
    "Source: NOAA NCEI daily-summaries (PRCP)",
    "Units: mm",
    "Temporal resolution: daily",
    "",
    "Event-date coverage:",
    ""
])

for station_id, group in stations.groupby("station_id"):
    counts = group["status"].value_counts()
    lines.append(
        f"- {station_id}: "
        f"{counts.get('complete', 0)} complete, "
        f"{counts.get('partial', 0)} partial, "
        f"{counts.get('missing', 0)} missing"
    )

lines.extend([
    "",
    "## 3. Annual Station Coverage",
    "",
    "| Station | Year | Valid days | Expected days | Coverage |",
    "|---|---:|---:|---:|---:|"
])

for _, row in station_daily.iterrows():
    lines.append(
        f"| {row['station_id']} | {int(row['year'])} | "
        f"{int(row['valid_days'])} | "
        f"{int(row['expected_days'])} | "
        f"{row['coverage_fraction']:.1%} |"
    )

lines.extend([
    "",
    "## 4. Important Limitations",
    "",
    "- Station observation cutoff times have not been verified.",
    "- Station daily totals cannot be treated as exact hourly event rainfall.",
    "- Missing observations and zero precipitation are distinct.",
    "- Station coverage varies substantially across years.",
    "- MRMS archive availability is incomplete for historical events.",
    "",
    "## 5. Reproducibility",
    "",
    "The processed data are stored in "
    "`data/processed/dc_flood_database.h5`.",
    "",
    "Analysis scripts read the HDF5 database directly."
])

output = Path("reports/data_quality_report.md")
output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("Report saved:", output)
print("MRMS events:", len(mrms))
print("Station-event records:", len(stations))
print("Annual station records:", len(station_daily))
