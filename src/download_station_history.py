
import requests
import pandas as pd
from io import StringIO
from pathlib import Path

stations = [
    "US1DCDC0014",
    "US1DCDC0026"
]

url = "https://www.ncei.noaa.gov/access/services/data/v1"

output_dir = Path("data/raw/stations")
output_dir.mkdir(parents=True, exist_ok=True)

for station_id in stations:

    params = {
        "dataset": "daily-summaries",
        "stations": station_id,
        "dataTypes": "PRCP",
        "startDate": "2015-01-01",
        "endDate": "2025-12-31",
        "units": "metric",
        "format": "csv",
        "includeAttributes": "true"
    }

    print("\nDownloading:", station_id)

    try:
        response = requests.get(
            url,
            params=params,
            timeout=120
        )
        response.raise_for_status()

        if not response.text.strip():
            print("No data returned")
            continue

        df = pd.read_csv(StringIO(response.text))

        output = output_dir / f"{station_id}_daily.csv"
        df.to_csv(output, index=False)

        print("Records:", len(df))
        print("First date:", df["DATE"].min())
        print("Last date:", df["DATE"].max())
        print("Missing PRCP:", df["PRCP"].isna().sum())
        print("Saved:", output)

    except (requests.RequestException, KeyError, ValueError) as e:
        print("ERROR:", e)
