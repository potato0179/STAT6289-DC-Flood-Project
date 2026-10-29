
import xarray as xr
import matplotlib.pyplot as plt

file_path = "data/raw/mrms/test_20250719_2300.grib2"

ds = xr.open_dataset(
    file_path,
    engine="cfgrib",
    backend_kwargs={"indexpath": ""}
)

# Select Washington, DC region
dc = ds.sel(
    latitude=slice(39.1, 38.7),
    longitude=slice(282.7, 283.2)
)

# Convert longitude to -180 to 180
dc = dc.assign_coords(longitude=dc.longitude - 360)

# Plot hourly precipitation
plt.figure(figsize=(9, 6))

dc["unknown"].plot(
    x="longitude",
    y="latitude",
    cmap="Blues",
    cbar_kwargs={"label": "1-hour precipitation (mm)"}
)

plt.title("NOAA MRMS Hourly Precipitation\nJuly 19, 2025, 22:00–23:00 UTC")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.tight_layout()
plt.savefig("figures/mrms_20250719_2300.png", dpi=200)
plt.close()

ds.close()

print("Map saved to figures/mrms_20250719_2300.png")
