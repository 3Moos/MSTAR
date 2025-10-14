import csv
import pandas
import pandas as pd #Allows for data manipulation
import numpy as np
import time
from pathlib import Path

current_time = time.localtime()
current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)

# BASE_DIR = Path("/Users/moose/Desktop/MSTAR/CSV data")
BASE_DIR = Path("../caclo4_data/caclo4")
#file = "/Users/moose/Desktop/MSTAR/curveGen/07082025 10% CaClO4 30% sat ink 18V NEW fine JSC W temp SENSOR 2 cell 7.5 NN.csv"
OUTPUT_NAME = f"analysis_csv_only - {time.strftime('%Y-%m-%d %H:%M:%S')}.csv"

# Columns we expect in each CSV
REQUIRED = [
    "Latest: Current (A)",
    "Latest: Temperature (°C)",
    "Latest: Oxygen Gas (ppm)",
    "Latest: Time (s)",
]

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
    for c in REQUIRED:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    rf = df[df["Latest: Current (A)"] > 0].copy()
    if rf.empty:
        print(f"[SKIP] {file_path.name}: no rows with Current > 0")
        return None


    rf = df[df["Latest: Current (A)"] > 0] #Gives all times
    first_row = rf.iloc[0] #inside df gives boolean values to rows that meet condition, outside df hides rows that are false.
    last_row = rf.iloc[-1]
    temp = rf["Latest: Temperature (°C)"]
    current = rf["Latest: Current (A)"]
    oxygen = rf["Latest: Oxygen Gas (ppm)"]
    times = rf["Latest: Time (s)"]
    times_start = int(first_row["Latest: Time (s)"])
    times_end = int(last_row["Latest: Time (s)"])
    temp_start = float(first_row["Latest: Temperature (°C)"])
    temp_end = float(last_row["Latest: Temperature (°C)"])
    current_start = float(first_row["Latest: Current (A)"])
    current_end = float(last_row["Latest: Current (A)"])
    av_temp = temp.mean()
    stdev_temp = temp.std() 
    temp_delta = float(temp_end - temp_start)
    av_current = current.mean()
    stdev_current = current.std()
    current_delta = float(current_end - current_start)
    oxygen_production = np.trapezoid(oxygen, times)

    run_time = int(times_end - times_start) #seconds

    #print(f"{av_temp}")
    #print(f"{stdev_temp}")
    #print(f"{integral}")

    #data = (f"{file}, 'conc', 'sat', {times_start}, {run_time}, {av_current}, {stdev_current}, 'dc', {av_temp}, {stdev_temp}, 'dt', {oxygen_production}")
    concentration = "conc"
    saturation = "sat"

    return [
        file_path.name, 
        concentration,
        saturation,
        times_start,
        run_time,
        av_current,
        stdev_current,
        current_delta,
        av_temp,
        stdev_temp,
        temp_delta,
        oxygen_production
    ]   


def main():
    rows = []
    csv_files = sorted(BASE_DIR.rglob("*.csv"))
    if not csv_files:
        print(f"No .csv files found in {BASE_DIR}")
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
