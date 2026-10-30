
import pandas as pd
import requests
import time
from pathlib import Path

# Read download queue
queue = pd.read_csv(
    "data/processed/mrms_download_queue.csv"
)

# Directory for downloaded archives
output_dir = Path("data/raw/mrms")
output_dir.mkdir(parents=True, exist_ok=True)

# Download all available MRMS files

results = []

for i, row in enumerate(queue.itertuples(), start=1):

    output_file = output_dir / row.filename

    print(f"[{i}/{len(queue)}] {row.filename}")

    if output_file.exists() and output_file.stat().st_size > 0:
        print("  Already downloaded")
        status = "existing"

    else:
        try:
            response = requests.get(
                row.url,
                timeout=60
            )
            response.raise_for_status()

            # Check gzip file signature
            if not response.content.startswith(b"\x1f\x8b"):
                raise ValueError("Downloaded content is not gzip")

            output_file.write_bytes(response.content)

            print("  Downloaded:", len(response.content), "bytes")
            status = "downloaded"

        except (requests.RequestException, ValueError) as e:
            print("  Failed:", e)
            status = "failed"

    results.append({
        "filename": row.filename,
        "status": status
    })

    time.sleep(0.3)

# Save download results
pd.DataFrame(results).to_csv(
    "reports/mrms_download_log.csv",
    index=False
)

print("\n=== Download Summary ===")
print(pd.Series([r["status"] for r in results]).value_counts())
