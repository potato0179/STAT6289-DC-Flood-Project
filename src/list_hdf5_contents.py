
import h5py

DATABASE = "data/processed/dc_flood_database.h5"


def list_database_contents():
    """Summarize available data directly from HDF5."""

    with h5py.File(DATABASE, "r") as h5:

        events = h5["events"]
        mrms = h5["gridded/mrms"]
        stations = h5["stations/precipitation"]

        print("=== DC Flood Database Contents ===")

        print("\nFlood events:", len(events))
        print("First event:", sorted(events.keys())[0])
        print("Last event:", sorted(events.keys())[-1])

        print("\nMRMS")
        print("Source: NOAA MRMS")
        print("Variable: precipitation")
        print("Available rasters:", len(mrms))

        times = sorted(
            group.attrs["time_utc"]
            for group in mrms.values()
        )

        print("First available:", times[0])
        print("Last available:", times[-1])

        print("\nDC Precipitation Stations")

        for station_id, group in stations.items():

            dates = group["date"].asstr()[:]

            print("\nStation:", station_id)
            print("Name:", group.attrs["station_name"])
            print("Variable:", group.attrs["variable"])
            print("Units:", group.attrs["units"])
            print("Records:", len(dates))
            print("First date:", dates[0])
            print("Last date:", dates[-1])


if __name__ == "__main__":
    list_database_contents()
