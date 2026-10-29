
import h5py
import pandas as pd
from pathlib import Path

DATABASE = "data/processed/dc_flood_database.h5"

records = []

with h5py.File(DATABASE, "r") as h5:

    mrms = h5["gridded/mrms"]

    # Collect available MRMS interval end times
    available = set()

    for group in mrms.values():
        timestamp = pd.Timestamp(
            group.attrs["interval_end_utc"]
        )
        available.add(timestamp)

    # Check each flood event
    for event_id, event in h5["events"].items():

        start = pd.Timestamp(event.attrs["start_utc"])
        end = pd.Timestamp(event.attrs["end_utc"])

        first = start.floor("h") + pd.Timedelta(hours=1)
        last = end.ceil("h")

        # Zero-duration events have no accumulation interval
        if end == start:
            records.append({
                "event_id": event_id,
                "start_utc": start,
                "end_utc": end,
                "expected_hours": 0,
                "available_hours": 0,
                "coverage_fraction": float("nan"),
                "status": "zero_duration"
            })
            continue

        expected = pd.date_range(
            first, last, freq="h"
        )

        found = sum(t in available for t in expected)

        total = len(expected)

        if found == total:
            status = "complete"
        elif found == 0:
            status = "missing"
        else:
            status = "partial"

        records.append({
            "event_id": event_id,
            "start_utc": start,
            "end_utc": end,
            "expected_hours": total,
            "available_hours": found,
            "coverage_fraction": found / total,
            "status": status
        })

coverage = pd.DataFrame(records)

# Save event-level coverage report
output = Path("reports/mrms_event_coverage.csv")
coverage.to_csv(output, index=False)

print("\n=== Event Coverage Summary ===")
print(coverage["status"].value_counts())

print("\n=== Hourly Coverage ===")
print("Expected hours:", coverage["expected_hours"].sum())
print("Available hours:", coverage["available_hours"].sum())

print("\n=== Coverage by Year ===")
coverage["year"] = coverage["start_utc"].dt.year

print(
    pd.crosstab(
        coverage["year"],
        coverage["status"]
    ).to_string()
)

print("\nReport saved:", output)
