
import h5py
import pandas as pd

file_path = "data/processed/dc_flood_database.h5"

with h5py.File(file_path, "r") as h5:

    mrms = h5["gridded/mrms/2025-07-19_2300"]

    rain_start = pd.Timestamp(mrms.attrs["interval_start_utc"])
    rain_end = pd.Timestamp(mrms.attrs["interval_end_utc"])

    matches = []

    for event_id in h5["events"]:
        event = h5["events"][event_id]

        event_start = pd.Timestamp(event.attrs["start_utc"])
        event_end = pd.Timestamp(event.attrs["end_utc"])

        # Check whether the time intervals overlap
        if event_start < rain_end and event_end > rain_start:
            matches.append(event_id)

    print("MRMS interval:", rain_start, "to", rain_end)
    print("Matching events:", matches)

    for event_id in matches:
        event = h5["events"][event_id]

        print("\nEvent:", event_id)
        print("Start:", event.attrs["start_utc"])
        print("End:", event.attrs["end_utc"])
