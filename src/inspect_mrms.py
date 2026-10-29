
import xarray as xr

# Open the downloaded MRMS file
file_path = "data/raw/mrms/test_20250719_2300.grib2"

ds = xr.open_dataset(
    file_path,
    engine="cfgrib",
    backend_kwargs={"indexpath": ""}
)

# Display the dataset structure
print("\n=== Dataset Structure ===")
print(ds)

# Display variables and units
print("\n=== Data Variables ===")
for name, variable in ds.data_vars.items():
    print("Variable:", name)
    print("Shape:", variable.shape)
    print("Units:", variable.attrs.get("GRIB_units", "Not specified"))
    print("Metadata:", variable.attrs)

# Display spatial coordinates
print("\n=== Coordinates ===")
for name, coordinate in ds.coords.items():
    print(name, coordinate.shape)

# Display time information
print("\n=== Time Information ===")
for name in ["time", "step", "valid_time"]:
    if name in ds.coords:
        print(name, ds[name].values)

ds.close()
