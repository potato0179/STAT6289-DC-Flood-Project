
import xarray as xr
import numpy as np

file_path = "data/raw/mrms/test_20250719_2300.grib2"

ds = xr.open_dataset(
    file_path,
    engine="cfgrib",
    backend_kwargs={"indexpath": ""}
)

# Washington, DC and surrounding area
lat_min, lat_max = 38.7, 39.1
lon_min, lon_max = -77.3, -76.8

# MRMS longitude uses 0-360 degrees
lon_min += 360
lon_max += 360

# Select the original grid cells
dc = ds.sel(
    latitude=slice(lat_max, lat_min),
    longitude=slice(lon_min, lon_max)
)

rain = dc["unknown"].values

print("Original shape:", ds["unknown"].shape)
print("DC subset shape:", rain.shape)

print("Latitude range:",
      float(dc.latitude.min()),
      float(dc.latitude.max()))

print("Longitude range (-180 to 180):",
      float(dc.longitude.min()) - 360,
      float(dc.longitude.max()) - 360)

print("Valid pixels:", np.isfinite(rain).sum())
print("Minimum:", np.nanmin(rain))
print("Maximum:", np.nanmax(rain))

ds.close()
