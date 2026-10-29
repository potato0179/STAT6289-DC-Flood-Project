
import h5py
import xarray as xr
import numpy as np

input_file = "data/raw/mrms/test_20250720_0000.grib2"
database = "data/processed/dc_flood_database.h5"

# Read the second hourly MRMS file
ds = xr.open_dataset(
    input_file,
    engine="cfgrib",
    backend_kwargs={"indexpath": ""}
)

# Select the same DC region
dc = ds.sel(
    latitude=slice(39.1, 38.7),
    longitude=slice(282.7, 283.2)
)

rain = dc["unknown"].values.astype(np.float32)
lat = dc.latitude.values
lon = dc.longitude.values - 360

# Add to the existing database
with h5py.File(database, "a") as h5:

    mrms = h5.require_group("gridded/mrms")

    event_name = "2025-07-20_0000"

    if event_name in mrms:
        raise ValueError("This MRMS interval already exists.")

    event = mrms.create_group(event_name)

    event.create_dataset(
        "precipitation",
        data=rain,
        compression="gzip"
    )

    event.create_dataset("latitude", data=lat)
    event.create_dataset("longitude", data=lon)

    event.attrs["source"] = "NOAA MRMS"
    event.attrs["product"] = "MultiSensor_QPE_01H_Pass2"
    event.attrs["units"] = "mm"
    event.attrs["time_utc"] = "2025-07-20T00:00:00Z"
    event.attrs["interval_start_utc"] = "2025-07-19T23:00:00Z"
    event.attrs["interval_end_utc"] = "2025-07-20T00:00:00Z"
    event.attrs["crs"] = "EPSG:4326"
    event.attrs["native_resolution_degrees"] = 0.01
    event.attrs["missing_value_encoding"] = "NaN"
    event.attrs["processing"] = (
        "Spatial subset; longitude converted to -180/180"
    )

ds.close()

print("Second MRMS raster successfully added to HDF5.")
print("Raster shape:", rain.shape)
print("Valid pixels:", np.isfinite(rain).sum())
print("Minimum precipitation:", np.nanmin(rain))
print("Maximum precipitation:", np.nanmax(rain))
