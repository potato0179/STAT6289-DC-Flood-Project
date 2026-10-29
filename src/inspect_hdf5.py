
import h5py
import numpy as np

file_path = "data/processed/dc_flood_database.h5"

with h5py.File(file_path, "r") as h5:

    print("=== Database Structure ===")

    def show_dataset(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(name, obj.shape, obj.dtype)

    h5.visititems(show_dataset)

    # Read precipitation data directly from HDF5
    event = h5["gridded/mrms/2025-07-19_2300"]

    rain = event["precipitation"][:]
    lat = event["latitude"][:]
    lon = event["longitude"][:]

    print("\n=== Data Validation ===")
    print("Raster shape:", rain.shape)
    print("Latitude points:", len(lat))
    print("Longitude points:", len(lon))
    print("Valid pixels:", np.isfinite(rain).sum())
    print("Minimum precipitation:", np.nanmin(rain))
    print("Maximum precipitation:", np.nanmax(rain))

    print("\n=== Metadata ===")
    for key, value in event.attrs.items():
        print(f"{key}: {value}")
