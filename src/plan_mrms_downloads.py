
import pandas as pd
from pathlib import Path

events = pd.read_csv(
    "data/processed/flood_events_validated.csv"
)

records = []

for i, row in events.iterrows():

    start = pd.Timestamp(row["start_utc"])
    end = pd.Timestamp(row["end_utc"])

    event_id = f"event_{i + 1:03d}"

    # Generate hourly MRMS interval end times
    first_hour = start.floor("h") + pd.Timedelta(hours=1)
    last_hour = end.ceil("h")

    if first_hour > last_hour:
        last_hour = first_hour

    hours = pd.date_range(
        first_hour,
        last_hour,
        freq="h"
    )

    for hour in hours:

        filename = (
            "MultiSensor_QPE_01H_Pass2_00.00_"
            + hour.strftime("%Y%m%d-%H%M%S")
            + ".grib2.gz"
        )

        url = (
            "https://mtarchive.geol.iastate.edu/"
            + hour.strftime("%Y/%m/%d")
            + "/mrms/ncep/MultiSensor_QPE_01H_Pass2/"
            + filename
        )

        records.append({
            "event_id": event_id,
            "time_utc": hour.isoformat(),
            "filename": filename,
            "url": url
        })

plan = pd.DataFrame(records)

# Remove duplicate hourly files shared by events
plan = plan.drop_duplicates(subset=["time_utc"])

output = Path("data/processed/mrms_download_plan.csv")
plan.to_csv(output, index=False)

print("Total events:", len(events))
print("Unique hourly MRMS files:", len(plan))
print("Download plan saved:", output)

print("\nFirst five planned files:")
print(plan.head().to_string(index=False))
