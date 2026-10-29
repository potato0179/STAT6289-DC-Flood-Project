
import pandas as pd
import h5py

# Load original event data
df = pd.read_csv("data/processed/flood_events_validated.csv")

# Assign unique event IDs
df["event_id"] = [
    f"event_{i:03d}" for i in range(1, len(df) + 1)
]

# Open existing HDF5 without overwriting it
with h5py.File("data/processed/dc_flood_database.h5", "a") as h5:

    events = h5.require_group("events")

    for _, row in df.iterrows():
        event_id = row["event_id"]

        event = events.require_group(event_id)

        event.attrs["start_utc"] = str(row["start_utc"])
        event.attrs["end_utc"] = str(row["end_utc"])
        event.attrs["begin_date"] = row["begin_date"]
        event.attrs["end_date"] = row["end_date"]
        event.attrs["duration_minutes"] = row["duration_minutes"]

    events.attrs["total_events"] = len(df)
    events.attrs["original_timezone"] = "Fixed EST (UTC-5)"
    events.attrs["source_file"] = "DC_flood_times.csv"

print("Successfully added", len(df), "flood events to HDF5.")
