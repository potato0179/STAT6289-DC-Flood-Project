
import h5py
import pandas as pd
import numpy as np

DATABASE = "data/processed/dc_flood_database.h5"

stations = {
    "US1DCDC0014": {
        "name": "WASHINGTON 5.1 NW, DC US",
        "latitude": 38.958091,
        "longitude": -77.08173
    },
    "US1DCDC0026": {
        "name": "WASHINGTON 2.6 NE, DC US",
        "latitude": 38.932715,
        "longitude": -76.983545
    }
}

with h5py.File(DATABASE, "a") as h5:

    station_root = h5.require_group("stations/precipitation")

    for station_id, info in stations.items():

        df = pd.read_csv(
            f"data/raw/stations/{station_id}_daily.csv",
            dtype={"PRCP_ATTRIBUTES": "string"}
        )

        df["DATE"] = pd.to_datetime(df["DATE"])
        df["PRCP"] = pd.to_numeric(df["PRCP"], errors="coerce")

        if station_id in station_root:
            print("Already stored:", station_id)
            continue

        group = station_root.create_group(station_id)

        dates = df["DATE"].dt.strftime("%Y-%m-%d").to_numpy()
        precipitation = df["PRCP"].to_numpy(dtype=np.float32)

        flags = (
            df["PRCP_ATTRIBUTES"]
            .fillna("")
            .to_numpy(dtype=str)
        )

        text_type = h5py.string_dtype(encoding="utf-8")

        group.create_dataset(
            "date",
            data=dates.astype(object),
            dtype=text_type
        )

        group.create_dataset(
            "precipitation",
            data=precipitation,
            compression="gzip"
        )

        group.create_dataset(
            "quality_attributes",
            data=flags.astype(object),
            dtype=text_type
        )

        group.attrs["station_id"] = station_id
        group.attrs["station_name"] = info["name"]
        group.attrs["latitude"] = info["latitude"]
        group.attrs["longitude"] = info["longitude"]
        group.attrs["crs"] = "EPSG:4326"
        group.attrs["source"] = "NOAA NCEI GHCN-Daily"
        group.attrs["variable"] = "PRCP"
        group.attrs["units"] = "mm"
        group.attrs["temporal_resolution"] = "daily"
        group.attrs["date_semantics"] = (
            "Source-reported observation date; "
            "daily accumulation boundary not yet verified"
        )
        group.attrs["missing_value_encoding"] = "NaN"
        group.attrs["raw_file"] = f"{station_id}_daily.csv"

        print("Added:", station_id, "| Records:", len(df))

print("\nDC precipitation stations integrated into HDF5.")
