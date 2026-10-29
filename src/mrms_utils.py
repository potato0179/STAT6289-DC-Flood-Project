
import numpy as np
import xarray as xr


def read_mrms_subset(file_path):
    """
    Read an MRMS GRIB2 file and extract
    Washington, DC and its surrounding area.
    """

    with xr.open_dataset(
        file_path,
        engine="cfgrib",
        backend_kwargs={"indexpath": ""}
    ) as ds:

        dc = ds.sel(
            latitude=slice(39.1, 38.7),
            longitude=slice(282.7, 283.2)
        )

        rain = dc["unknown"].values.astype(np.float32).copy()
        latitude = dc.latitude.values.copy()
        longitude = dc.longitude.values.copy() - 360

        time_utc = str(dc.valid_time.values)

    return {
        "precipitation": rain,
        "latitude": latitude,
        "longitude": longitude,
        "time_utc": time_utc,
        "units": "mm"
    }


if __name__ == "__main__":

    result = read_mrms_subset(
        "data/raw/mrms/test_20250719_2300.grib2"
    )

    print("Shape:", result["precipitation"].shape)
    print("Time:", result["time_utc"])
    print("Maximum:", np.nanmax(result["precipitation"]))
    print("Units:", result["units"])
