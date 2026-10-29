
import pandas as pd
from pathlib import Path

stations = ["US1DCDC0014", "US1DCDC0026"]

records = []

for station_id in stations:

    path = Path(f"data/raw/stations/{station_id}_daily.csv")
    df = pd.read_csv(path)

    df["DATE"] = pd.to_datetime(df["DATE"])
    df["PRCP"] = pd.to_numeric(df["PRCP"], errors="coerce")

    # Check the observation period
    first = df["DATE"].min()
    last = df["DATE"].max()

    expected_dates = pd.date_range(first, last, freq="D")

    # Count unique dates with valid precipitation
    valid_dates = df.loc[
        df["PRCP"].notna(), "DATE"
    ].nunique()

    coverage = valid_dates / len(expected_dates)

    print(f"\n=== {station_id} ===")
    print("Expected days:", len(expected_dates))
    print("Recorded rows:", len(df))
    print("Valid precipitation days:", valid_dates)
    print("Missing/invalid days:",
          len(expected_dates) - valid_dates)
    print("Coverage:", f"{coverage:.2%}")

    # Calculate coverage by year
    for year in range(first.year, last.year + 1):

        year_start = max(first, pd.Timestamp(year, 1, 1))
        year_end = min(last, pd.Timestamp(year, 12, 31))

        days = pd.date_range(year_start, year_end, freq="D")

        valid = df[
            (df["DATE"].dt.year == year)
            & df["PRCP"].notna()
        ]["DATE"].nunique()

        records.append({
            "station_id": station_id,
            "year": year,
            "expected_days": len(days),
            "valid_days": valid,
            "coverage_fraction": valid / len(days)
        })

report = pd.DataFrame(records)

report.to_csv(
    "reports/dc_station_coverage.csv",
    index=False
)

print("\n=== Coverage by Year ===")
print(
    report.pivot(
        index="year",
        columns="station_id",
        values="coverage_fraction"
    ).round(3).to_string()
)

print("\nSaved: reports/dc_station_coverage.csv")
