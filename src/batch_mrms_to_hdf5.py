
import gzip
import tempfile
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

from mrms_utils import read_mrms_subset

QUEUE = "data/processed/mrms_download_queue.csv"
DATABASE = "data/processed/dc_flood_database.h5"
RAW_DIR = Path("data/raw/mrms")

queue = pd.read_csv(QUEUE)

added = 0
skipped = 0
failed = 0

with h5py.File(DATABASE, "a") as h5:

    mrms = h5.require_group("gridded/mrms")

    for _, row in queue.iterrows():

        # Use UTC timestamp to identify each raster
        timestamp = pd.Timestamp(row["time_utc"])

        group_name = timestamp.strftime("%Y-%m-%d_%H%M")
        compressed_file = RAW_DIR / row["filename"]

        # Do not overwrite existing observations
        if group_name in mrms:
            skipped += 1
            continue

        if not compressed_file.exists():
            print("MISSING:", compressed_file.name)
            failed += 1
            continue

        try:
            # Temporarily decompress one GRIB2 file
            with tempfile.TemporaryDirectory() as tmp:
                grib_file = Path(tmp) / "data.grib2"

                with gzip.open(compressed_file, "rb") as source:
                    with open(grib_file, "wb") as target:
                        target.write(source.read())

                data = read_mrms_subset(str(grib_file))

            # Check raster dimensions
            rain = data["precipitation"]

            if rain.shape != (40, 50):
                raise ValueError("Unexpected raster shape")

            # Create one HDF5 group per hour
            group = mrms.create_group(group_name)

            group.create_dataset(
                "precipitation",
                data=rain,
                compression="gzip"
            )

            group.create_dataset(
                "latitude",
                data=data["latitude"]
            )

            group.create_dataset(
                "longitude",
                data=data["longitude"]
            )

            # Store metadata
            group.attrs["source"] = "NOAA MRMS"
            group.attrs["product"] = "MultiSensor_QPE_01H_Pass2"
            group.attrs["units"] = "mm"
            group.attrs["crs"] = "EPSG:4326"
            group.attrs["native_resolution_degrees"] = 0.01

            group.attrs["time_utc"] = timestamp.isoformat()
            group.attrs["interval_start_utc"] = (
                timestamp - pd.Timedelta(hours=1)
            ).isoformat()
            group.attrs["interval_end_utc"] = timestamp.isoformat()

            group.attrs["missing_value_encoding"] = "NaN"
            group.attrs["processing"] = (
                "Spatial subset; longitude converted to -180/180"
            )
            group.attrs["source_filename"] = row["filename"]

            added += 1

        except Exception as e:
            print("FAILED:", compressed_file.name, e)
            failed += 1

    print("\n=== Processing Summary ===")
    print("Added:", added)
    print("Already present:", skipped)
    print("Failed:", failed)
    print("Total stored MRMS rasters:", len(mrms))
