
import pandas as pd
import requests
import time

plan = pd.read_csv(
    "data/processed/mrms_candidate_files.csv"
)

results = []

session = requests.Session()

for i, row in plan.iterrows():
    url = row["url"]

    try:
        response = session.head(
            url,
            timeout=15,
            allow_redirects=True
        )

        status = response.status_code
        size = response.headers.get("Content-Length")

    except requests.RequestException:
        status = "connection_error"
        size = None

    results.append({
        **row.to_dict(),
        "http_status": status,
        "file_size_bytes": size
    })

    if (i + 1) % 25 == 0:
        print(f"Checked {i + 1}/{len(plan)} files")

    time.sleep(0.2)

results_df = pd.DataFrame(results)

results_df.to_csv(
    "reports/mrms_availability.csv",
    index=False
)

print("\n=== Availability Summary ===")
print(results_df["http_status"].value_counts())

print("\n=== Availability by Year ===")
results_df["year"] = pd.to_datetime(
    results_df["time_utc"], utc=True
).dt.year

print(
    pd.crosstab(
        results_df["year"],
        results_df["http_status"]
    ).to_string()
)

print("\nSaved: reports/mrms_availability.csv")
