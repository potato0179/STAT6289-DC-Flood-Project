
import h5py
import xarray as xr
import numpy as np
from pathlib import Path

# Input and output paths
input_file = "data/raw/mrms/test_20250719_2300.grib2"
output_file = Path("data/processed/dc_flood_database.h5")

# Open MRMS data
ds = xr.open_dataset(
    input_file,
    engine="cfgrib",
    backend_kwargs={"indexpath": ""}
)

# Subset to Washington, DC region
dc = ds.sel(
    latitude=slice(39.1, 38.7),
    longitude=slice(282.7, 283.2)
)

rain = dc["unknown"].values.astype(np.float32)
lat = dc.latitude.values
lon = dc.longitude.values - 360

# Create HDF5 database
with h5py.File(output_file, "w") as h5:

    # General metadata
    h5.attrs["project"] = "STAT 6289 DC Flood Data Project"
    h5.attrs["description"] = "Environmental data for DC flood events"

    # MRMS group
    mrms = h5.create_group("gridded/mrms")

    event = mrms.create_group("2025-07-19_2300")

    event.create_dataset(
        "precipitation",
        data=rain,
        compression="gzip"
    )

    event.create_dataset("latitude", data=lat)
    event.create_dataset("longitude", data=lon)

    # Metadata
    event.attrs["source"] = "NOAA MRMS"
    event.attrs["product"] = "MultiSensor_QPE_01H_Pass2"
    event.attrs["units"] = "mm"
    event.attrs["time_utc"] = "2025-07-19T23:00:00Z"
    event.attrs["interval_start_utc"] = "2025-07-19T22:00:00Z"
    event.attrs["interval_end_utc"] = "2025-07-19T23:00:00Z"
    event.attrs["crs"] = "EPSG:4326"
    event.attrs["native_resolution_degrees"] = 0.01
    event.attrs["missing_value_encoding"] = "NaN"
    event.attrs["processing"] = "Spatial subset; longitude converted to -180/180"

ds.close()

print("HDF5 database created:", output_file)
