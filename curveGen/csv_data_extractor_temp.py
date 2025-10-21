import csv
import pandas as pd  # Allows for data manipulation
import numpy as np
import time
from pathlib import Path

current_time = time.localtime()
current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)

# Resolve BASE_DIR relative to this script so the script finds files
# whether it's executed from the repo root, the curvegen folder, or elsewhere.
BASE_DIR = Path(__file__).resolve().parent / "caclo4_data" / "caclo4"
OUTPUT_NAME = f"analysis_csv_only - {time.strftime('%Y-%m-%d %H-%M-%S')}.csv"

# Columns we expect in each CSV
REQUIRED = [
    "Latest: Current (A)",
    "Latest: Temperature (°C)",
    "Latest: Oxygen Gas (ppm)",
    "Latest: Time (s)",
]

# Exactly how many contiguous rows to analyze after power-on
TARGET_ROWS = 1001


def analyze_one(file_path: Path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"[SKIP] {file_path.name}: failed to read CSV ({e})")
        return None

    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        print(f"[SKIP] {file_path.name}: missing columns: {missing}")
        return None

    # Coerce numerics
    for c in REQUIRED:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    cur = df["Latest: Current (A)"]

    # 1) First power-on index: first row where current > 0
    mask = cur > 0
    if not mask.any():
        print(f"[SKIP] {file_path.name}: no rows with Current > 0")
        return None
    start_idx = mask.idxmax()  # first True index (first >0)

    # 2) Find the end of the first contiguous >0 block
    contiguous_mask = (cur[start_idx:] > 0)
    breaks = (~contiguous_mask).to_numpy().nonzero()[0]  # positions of first False in the block
    if len(breaks) > 0:
        block_end_inclusive = start_idx + breaks[0] - 1
    else:
        block_end_inclusive = df.index[-1]

    # 3) Require TARGET_ROWS contiguous >0 rows starting at start_idx
    needed_end = start_idx + TARGET_ROWS - 1
    if block_end_inclusive < needed_end:
        have = block_end_inclusive - start_idx + 1
        print(f"[SKIP] {file_path.name}: only {have} contiguous >0 rows after power-on (< {TARGET_ROWS})")
        return None

    # 4) Take EXACTLY those TARGET_ROWS contiguous rows from the ORIGINAL df
    rf = df.loc[start_idx:needed_end].copy()

    # 5) Compute stats within this window
    first_row = rf.iloc[0]
    last_row  = rf.iloc[-1]

    times   = rf["Latest: Time (s)"]
    temp    = rf["Latest: Temperature (°C)"]
    current = rf["Latest: Current (A)"]
    oxygen  = rf["Latest: Oxygen Gas (ppm)"]

    # Runtime uses actual timestamps; with 1 Hz data and 1000 rows, expect ~999 s span
    times_start = int(first_row["Latest: Time (s)"])
    times_end   = int(last_row["Latest: Time (s)"])
    run_time    = int(times_end - times_start)

    temp_start    = float(first_row["Latest: Temperature (°C)"])
    temp_end      = float(last_row["Latest: Temperature (°C)"])
    current_start = float(first_row["Latest: Current (A)"])
    current_end   = float(last_row["Latest: Current (A)"])

    av_temp       = float(temp.mean())
    stdev_temp    = float(temp.std(ddof=1))
    temp_delta    = float(temp_end - temp_start)

    av_current    = float(current.mean())
    stdev_current = float(current.std(ddof=1))
    current_delta = float(current_end - current_start)

    # Integrate oxygen over time; drop rows with NaNs in either series
    valid = oxygen.notna() & times.notna()
    if valid.any():
        oxygen_production = float(np.trapz(oxygen[valid], times[valid]))
    else:
        oxygen_production = float("nan")

     #Subract initial O2 from remaining O2 values to get produced O2
    if valid.any():
        oxy_baseline = float(first_row["Latest: Oxygen Gas (ppm)"])
        oxy_rel = oxygen - oxy_baseline
        # oxy_rel = oxy_rel.clip(lower=0)  # optional: prevent negative contributions
        oxygen_production = float(np.trapz(oxy_rel[valid], times[valid]))
    else:
        oxygen_production = float("nan")

    return [
        file_path.name,
        "conc",
        "sat",
        times_start,
        run_time,
        av_current,
        stdev_current,
        current_delta,
        av_temp,
        stdev_temp,
        temp_delta,
        oxygen_production,
    ]





def main():
    rows = []
    csv_files = sorted(BASE_DIR.rglob("*.csv"))
    if not csv_files:
        print(f"No .csv files found in {BASE_DIR} (resolved: {BASE_DIR.resolve()})")
        # helpful diagnostic: list the parent dir contents for debugging
        try:
            print(f"Parent dir contents: {list(BASE_DIR.parent.iterdir())}")
        except Exception:
            pass
        return

    for fp in csv_files:
        row = analyze_one(fp)
        if row is not None:
            rows.append(row)

    if not rows:
        print("No analyzable CSVs produced results.")
        return

    header = [
        "File Name","Concentration","Saturation",
        "Start time","Run time",
        "Mean Current","Current stdev","Delta Current",
        "Mean Temp","Temp STDEV","Delta Temp",
        "Oxygen Production"
    ]

    out_path = BASE_DIR.parent / OUTPUT_NAME
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

    print(f"analysis complete. Wrote {len(rows)} rows -> {out_path}")


if __name__ == "__main__":
    main()
