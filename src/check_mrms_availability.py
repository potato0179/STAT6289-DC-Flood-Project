
import pandas as pd
import requests
from pathlib import Path

plan = pd.read_csv(
    "data/processed/mrms_candidate_files.csv"
)

results = []

for i, row in enumerate(plan.itertuples(), start=1):

    try:
        response = requests.head(
            row.url,
            timeout=20,
            allow_redirects=True
        )
        status = response.status_code
        size = response.headers.get("Content-Length")

    except requests.RequestException:
        status = None
        size = None

    results.append({
        "event_id": row.event_id,
        "time_utc": row.time_utc,
        "filename": row.filename,
        "url": row.url,
        "http_status": status,
        "file_size_bytes": size
    })

    print(f"[{i}/{len(plan)}] HTTP {status}")

output = Path("reports/mrms_availability.csv")

pd.DataFrame(results).to_csv(output, index=False)

print("\nAvailability report saved:", output)
print("Files checked:", len(results))
