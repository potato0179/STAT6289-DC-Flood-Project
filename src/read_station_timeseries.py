
import h5py
import pandas as pd

DATABASE = "data/processed/dc_flood_database.h5"


def get_station_timeseries(station_id, start_date, end_date):
    """Retrieve daily precipitation directly from HDF5."""

    with h5py.File(DATABASE, "r") as h5:

        group = h5["stations/precipitation"][station_id]

        dates = group["date"].asstr()[:]
        precipitation = group["precipitation"][:]
        flags = group["quality_attributes"].asstr()[:]

        df = pd.DataFrame({
            "date": pd.to_datetime(dates),
            "precipitation_mm": precipitation,
            "quality_attributes": flags
        })

    # Select the requested date range
    mask = (
        (df["date"] >= pd.Timestamp(start_date))
        & (df["date"] <= pd.Timestamp(end_date))
    )

    return df.loc[mask].reset_index(drop=True)


if __name__ == "__main__":

    for station_id in ["US1DCDC0014", "US1DCDC0026"]:

        result = get_station_timeseries(
            station_id,
            "2021-09-15",
            "2021-09-18"
        )

        print("\nStation:", station_id)
        print(result.to_string(index=False))
