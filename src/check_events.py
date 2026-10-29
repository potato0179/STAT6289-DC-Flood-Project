
import pandas as pd
from pathlib import Path

# Locate the original CSV
csv_path = Path("data/raw/DC_flood_times.csv")

# Read the flood events
df = pd.read_csv(csv_path)

# Display basic information
print("Total events:", len(df))
print("\nColumns:", df.columns.tolist())
print("\nFirst five events:")
print(df.head())

# Check missing values
print("\nMissing values:")
print(df.isna().sum())

# Parse event dates and times
df["start"] = pd.to_datetime(
    df["begin_date"].astype(str) + " " + df["begin_time"].astype(str),
    errors="coerce"
)

df["end"] = pd.to_datetime(
    df["end_date"].astype(str) + " " + df["end_time"].astype(str),
    errors="coerce"
)

# Check invalid timestamps
print("\nInvalid start times:", df["start"].isna().sum())
print("Invalid end times:", df["end"].isna().sum())

# Check event duration
df["duration_minutes"] = (
    df["end"] - df["start"]
).dt.total_seconds() / 60

print("\nZero-duration events:",
      (df["duration_minutes"] == 0).sum())

print("Negative-duration events:",
      (df["duration_minutes"] < 0).sum())

print("\nDate range:")
print(df["start"].min(), "to", df["end"].max())

# Convert fixed EST (UTC-5) to UTC
df["start_utc"] = (
    df["start"].dt.tz_localize("Etc/GMT+5").dt.tz_convert("UTC")
)

df["end_utc"] = (
    df["end"].dt.tz_localize("Etc/GMT+5").dt.tz_convert("UTC")
)

# Display a sample event
print("\nOriginal EST and converted UTC:")
print(
    df[["start", "start_utc", "end", "end_utc"]].tail(1)
)

# Save the validated event index
output_path = Path("data/processed/flood_events_validated.csv")
df.to_csv(output_path, index=False)

print("\nSaved validated events to:", output_path)

# Count flood events by year
df["year"] = df["start_utc"].dt.year

year_counts = df.groupby("year").size()

print("\nFlood events by year:")
print(year_counts.to_string())

# Preliminary MRMS historical period
before_2012 = (df["year"] < 2012).sum()
from_2012 = (df["year"] >= 2012).sum()

print("\nEvents before 2012:", before_2012)
print("Events from 2012 onward:", from_2012)
