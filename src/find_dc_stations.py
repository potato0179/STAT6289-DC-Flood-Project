
import requests

url = "https://www.ncei.noaa.gov/access/services/search/v1/data"

params = {
    "dataset": "daily-summaries",
    "bbox": "39.0,-77.12,38.79,-76.90",
    "startDate": "2021-01-01",
    "endDate": "2021-12-31",
    "limit": 1000
}

response = requests.get(url, params=params, timeout=60)
response.raise_for_status()

data = response.json()

print("=== NOAA Station Search ===")
print("Response type:", type(data).__name__)
print("Response preview:")
print(str(data)[:3000])

print("\n=== Response Keys ===")
print(list(data.keys()))

print("\n=== DC Station IDs ===")
stations = data.get("stations", {}).get("buckets", [])

for station in stations:
    station_id = station.get("key", "")

    if station_id.startswith("US1DCDC"):
        print(station_id)

print("\n=== First Search Result ===")
results = data.get("results", [])

if results:
    print(results[0])
else:
    print("No detailed results found.")

print("\n=== DC Station Details ===")

for result in data.get("results", []):
    for station in result.get("stations", []):

        station_id = station.get("id", "")

        if station_id.startswith("US1DCDC"):
            coords = result.get("centroid", [None, None])

            print(
                "ID:", station_id,
                "| Name:", station.get("name", "Unknown"),
                "| Coordinates:", coords,
                "| Start:", result.get("startDate"),
                "| End:", result.get("endDate")
            )
