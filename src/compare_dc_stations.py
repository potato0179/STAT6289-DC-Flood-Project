
import requests
import pandas as pd
from io import StringIO

stations = [
    "US1DCDC0009",
    "US1DCDC0014",
    "US1DCDC0026",
    "US1DCDC0031",
    "US1DCDC0034"
]

url = "https://www.ncei.noaa.gov/access/services/data/v1"

for station_id in stations:

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

    print("\nStation:", station_id)

    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()

        if not response.text.strip():
            print("No records returned")
            continue

        df = pd.read_csv(StringIO(response.text))

        if df.empty:
            print("No records returned")
        else:
            print(df.to_string(index=False))

    except (requests.RequestException, pd.errors.ParserError) as e:
        print("ERROR:", e)
