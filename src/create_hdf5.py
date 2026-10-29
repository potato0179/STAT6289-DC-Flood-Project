
import h5py
from pathlib import Path

output_file = Path(
    "data/processed/dc_flood_database.h5"
)

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Protect the existing database
if output_file.exists():
    print("Database already exists:", output_file)
    print("No changes made.")

else:
    with h5py.File(output_file, "w") as h5:

        h5.attrs["project"] = (
            "STAT 6289 DC Flood Data Project"
        )

        h5.attrs["description"] = (
            "Environmental database for DC flood events"
        )

        h5.create_group("events")
        h5.create_group("gridded/mrms")
        h5.create_group("stations/precipitation")

    print("New HDF5 database created:", output_file)
