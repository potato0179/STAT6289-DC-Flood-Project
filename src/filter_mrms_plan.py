
import pandas as pd

plan = pd.read_csv(
    "data/processed/mrms_download_plan.csv"
)

plan["time_utc"] = pd.to_datetime(
    plan["time_utc"], utc=True
)

# Approximate start of MTArchive MRMS coverage
archive_start = pd.Timestamp("2014-10-01", tz="UTC")

# Split potential and historical unavailable records
candidates = plan[
    plan["time_utc"] >= archive_start
].copy()

older = plan[
    plan["time_utc"] < archive_start
].copy()

# Save both groups
candidates.to_csv(
    "data/processed/mrms_candidate_files.csv",
    index=False
)

older.to_csv(
    "data/processed/mrms_pre_archive_files.csv",
    index=False
)

print("Total planned files:", len(plan))
print("Before archive period:", len(older))
print("Files requiring availability checks:", len(candidates))

print("\nCandidate files by year:")
print(
    candidates.groupby(
        candidates["time_utc"].dt.year
    ).size().to_string()
)
