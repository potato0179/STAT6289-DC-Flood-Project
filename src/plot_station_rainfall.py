
import matplotlib.pyplot as plt
import pandas as pd
from read_station_timeseries import get_station_timeseries

stations = {
    "US1DCDC0014": "Washington 5.1 NW",
    "US1DCDC0026": "Washington 2.6 NE"
}

fig, ax = plt.subplots(figsize=(9, 5))

for station_id, name in stations.items():

    df = get_station_timeseries(
        station_id,
        "2021-09-15",
        "2021-09-18"
    )

   
    # Include missing dates explicitly
    all_dates = pd.date_range(
        df["date"].min(),
        df["date"].max(),
        freq="D"
    )

    df = (
        df.set_index("date")
        .reindex(all_dates)
    )

    ax.plot(
        df.index,
        df["precipitation_mm"],
        marker="o",
        linewidth=2,
        label=name
    )


ax.set_title(
    "DC Station Daily Precipitation\n"
    "September 15–18, 2021"
)

ax.set_xlabel("NOAA-reported observation date")
ax.set_ylabel("Daily precipitation (mm)")
ax.legend()
ax.grid(alpha=0.3)

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    "figures/dc_station_rainfall_202109.png",
    dpi=200
)

plt.close()

print("Station precipitation figure saved successfully.")
