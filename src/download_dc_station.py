
import requests
import pandas as pd
from io import StringIO
from pathlib import Path

station_id = "US1DCDC0014"

url = "https://www.ncei.noaa.gov/access/services/data/v1"

params = {
    "dataset": "daily-summaries",
    "stations": station_id,
    "dataTypes": "PRCP",
    "startDate": "2021-09-15",
    "endDate": "2021-09-18",
    "units": "metric",
    "format": "csv",
    "includeAttributes": "true"
}

response = requests.get(
    url,
    params=params,
    timeout=60
)

response.raise_for_status()

print("HTTP status:", response.status_code)
print("\nResponse:")
print(response.text[:2000])

if response.text.strip():
    df = pd.read_csv(StringIO(response.text))

    output = Path(
        "data/raw/dc_station_test.csv"
    )

    df.to_csv(output, index=False)

    print("\nRows:", len(df))
    print("Columns:", df.columns.tolist())
    print("Saved:", output)
