
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

plan = pd.read_csv(
    "data/processed/mrms_candidate_files.csv"
)

plan["year"] = pd.to_datetime(
    plan["time_utc"], utc=True
).dt.year

# Test one file from each selected year
for year in [2015, 2018, 2022, 2025]:

    subset = plan[plan["year"] == year]

    if subset.empty:
        continue

    url = subset.iloc[0]["url"]

    print(f"\nYear: {year}")

    try:
        request = Request(url, method="HEAD")

        with urlopen(request, timeout=20) as response:
            print("HTTP status:", response.status)
            print(
                "Content type:",
                response.headers.get("Content-Type")
            )
            print(
                "File size:",
                response.headers.get("Content-Length")
            )

    except HTTPError as e:
        print("HTTP status:", e.code)

    except URLError as e:
        print("Connection error:", e.reason)

    except TimeoutError:
        print("Connection timed out")
