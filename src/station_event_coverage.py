
import pandas as pd
from pathlib import Path

events = pd.read_csv(
    "data/processed/flood_events_validated.csv"
)

stations = ["US1DCDC0014", "US1DCDC0026"]

records = []

for station_id in stations:

    df = pd.read_csv(
        f"data/raw/stations/{station_id}_daily.csv"
    )

    df["DATE"] = pd.to_datetime(df["DATE"])
    df["PRCP"] = pd.to_numeric(df["PRCP"], errors="coerce")

    valid_dates = set(
        df.loc[df["PRCP"].notna(), "DATE"]
    )

    for i, event in events.iterrows():

        # Use original reported dates, not UTC dates,
        # for preliminary daily coverage screening.
        start = pd.Timestamp(event["begin_date"])
        end = pd.Timestamp(event["end_date"])

        dates = pd.date_range(start, end, freq="D")

        found = sum(date in valid_dates for date in dates)

        if found == len(dates):
            status = "complete"
        elif found == 0:
            status = "missing"
        else:
            status = "partial"

        records.append({
            "station_id": station_id,
            "event_id": f"event_{i + 1:03d}",
            "expected_days": len(dates),
            "valid_days": found,
            "status": status
        })

report = pd.DataFrame(records)

output = Path("reports/dc_station_event_coverage.csv")
report.to_csv(output, index=False)

print("=== Station Event Coverage ===")
print(
    pd.crosstab(
        report["station_id"],
        report["status"]
    ).to_string()
)

print("\nSaved:", output)
