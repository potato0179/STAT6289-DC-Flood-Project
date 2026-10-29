
import pandas as pd
from pathlib import Path

# Read the availability report
df = pd.read_csv("reports/mrms_availability.csv")

# Select files returning HTTP 200
available = df[
    pd.to_numeric(df["http_status"], errors="coerce") == 200
].copy()

# Remove duplicates and sort by time
available = available.drop_duplicates(subset=["time_utc"])
available = available.sort_values("time_utc")

# Save the download queue
output = Path("data/processed/mrms_download_queue.csv")
available.to_csv(output, index=False)

print("Files ready for download:", len(available))
print("Download queue saved:", output)

print("\nFiles by year:")
available["year"] = pd.to_datetime(
    available["time_utc"], utc=True
).dt.year

print(available.groupby("year").size().to_string())
