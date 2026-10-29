
import h5py
import pandas as pd
import numpy as np

DATABASE = "data/processed/dc_flood_database.h5"


def get_event_rasters(event_id, time_utc=None):
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

                if time_utc is not None:
                    requested_time = pd.Timestamp(time_utc)

                    if requested_time.tzinfo is None:
                        raise ValueError(
                            "time_utc must include a timezone"
                        )

                    if rain_end != requested_time:
                        continue

                results.append({
                    "time": rain_end,
                    "precipitation": group["precipitation"][:],
                    "latitude": group["latitude"][:],
                    "longitude": group["longitude"][:],
                    "units": group.attrs["units"]
                })

    return sorted(results, key=lambda item: item["time"])


if __name__ == "__main__":

    rasters = get_event_rasters(
        "event_125",
        "2025-07-19T23:00:00Z"
    )

    print("=== Selected MRMS Raster ===")
    print("Matching rasters:", len(rasters))

    for raster in rasters:
        print("Time:", raster["time"])
        print("Shape:", raster["precipitation"].shape)
        print("Maximum:", np.nanmax(raster["precipitation"]))
        print("Units:", raster["units"])
