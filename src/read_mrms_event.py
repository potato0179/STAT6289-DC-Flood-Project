
import h5py
import pandas as pd
import numpy as np

DATABASE = "data/processed/dc_flood_database.h5"


def get_event_rasters(event_id):
    """Read MRMS rasters overlapping a flood event."""

    results = []

    with h5py.File(DATABASE, "r") as h5:

        event = h5["events"][event_id]
        start = pd.Timestamp(event.attrs["start_utc"])
        end = pd.Timestamp(event.attrs["end_utc"])

        for name, group in h5["gridded/mrms"].items():

            rain_start = pd.Timestamp(
                group.attrs["interval_start_utc"]
            )
            rain_end = pd.Timestamp(
                group.attrs["interval_end_utc"]
            )

            if rain_start < end and rain_end > start:
                results.append({
                    "time": rain_end,
                    "precipitation": group["precipitation"][:],
                    "latitude": group["latitude"][:],
                    "longitude": group["longitude"][:],
                    "units": group.attrs["units"]
                })

    return sorted(results, key=lambda item: item["time"])


# Demonstrate the function
rasters = get_event_rasters("event_125")

print("Event: event_125")
print("Number of matching MRMS rasters:", len(rasters))

for raster in rasters:
    print(
        raster["time"],
        "Shape:", raster["precipitation"].shape,
        "Maximum:", np.nanmax(raster["precipitation"]),
        raster["units"]
    )
