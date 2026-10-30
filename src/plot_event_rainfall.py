
import h5py
import numpy as np
import matplotlib.pyplot as plt

database = "data/processed/dc_flood_database.h5"

with h5py.File(database, "r") as h5:

    mrms = h5["gridded/mrms"]

    first = mrms["2025-07-19_2300"]
    second = mrms["2025-07-20_0000"]

    rain1 = first["precipitation"][:]
    rain2 = second["precipitation"][:]

    lat = first["latitude"][:]
    lon = first["longitude"][:]

    # Confirm both rasters share the same grid
    assert np.array_equal(lat, second["latitude"][:])
    assert np.array_equal(lon, second["longitude"][:])

    # Preserve missing values
    total_rain = rain1 + rain2

    print("Maximum two-hour precipitation:",
          np.nanmax(total_rain), "mm")

    print("Valid pixels:",
          np.isfinite(total_rain).sum())

    # Create the map
    fig, ax = plt.subplots(figsize=(9, 6))

    image = ax.pcolormesh(
        lon,
        lat,
        total_rain,
        cmap="Blues",
        shading="nearest"
    )

    fig.colorbar(
        image,
        ax=ax,
        label="Two-hour accumulated precipitation (mm)"
    )

    ax.set_title(
        "NOAA MRMS — Event 125\n"
        "July 19, 22:00 – July 20, 00:00 UTC (2025)"
    )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    plt.tight_layout()

    plt.savefig(
        "figures/event_125_two_hour_rainfall.png",
        dpi=200
    )

    plt.close()

print("Figure saved successfully.")
