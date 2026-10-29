
import h5py
import numpy as np

with h5py.File("data/processed/dc_flood_database.h5", "r") as h5:

    mrms = h5["gridded/mrms"]

    rain1 = mrms["2025-07-19_2300/precipitation"][:]
    rain2 = mrms["2025-07-20_0000/precipitation"][:]

    total = rain1 + rain2

    print("First hour:")
    print("  Maximum:", np.nanmax(rain1))
    print("  Mean:", np.nanmean(rain1))
    print("  Rainy pixels:", np.sum(rain1 > 0))

    print("\nSecond hour:")
    print("  Maximum:", np.nanmax(rain2))
    print("  Mean:", np.nanmean(rain2))
    print("  Rainy pixels:", np.sum(rain2 > 0))

    print("\nTwo-hour total:")
    print("  Maximum:", np.nanmax(total))
    print("  Mean:", np.nanmean(total))
    print("  Rainy pixels:", np.sum(total > 0))

    print("\nNegative values:",
          np.sum(rain1 < 0) + np.sum(rain2 < 0))
