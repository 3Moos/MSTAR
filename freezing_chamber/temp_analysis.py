import csv
import pandas as pd  # Allows for data manipulation
import numpy as np
import time
from pathlib import Path
import os
from datetime import datetime

# -------------------- CONFIG --------------------
# Make sure to change hardcoded file names before running
# Make sure to change hard-coded values of the Temp Sensors "ts1, ts2, etc." to match actual sensor-to-cell mapping
# Make sure to change the hardcoded values in the average_map dictionary to match the actual cell numbers and average cells used for extrapolation
# Also change the hardcoded order list to match the actual sensor-to-cell mapping
# Make sure to change the hardcoded experiment name below

experiment_name = "CaNaMg_55pct_60pct_08292025"
timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')

# -------------------- INPUT FILES --------------------
df_p1 = pd.read_csv('/Users/moose/Documents/MSTAR_Code/MSTAR/freezing_chamber/freezing_data/NaCaMg_25%_20%_15%_10%_5%/logs 10-24-2025-Fri 17-25-07-PM/ power 1 10-24-2025-Fri 17-25-07-PM.csv')
df_p2 = pd.read_csv('/Users/moose/Documents/MSTAR_Code/MSTAR/freezing_chamber/freezing_data/NaCaMg_25%_20%_15%_10%_5%/logs 10-24-2025-Fri 17-25-07-PM/ power 2 10-24-2025-Fri 17-25-07-PM.csv')
df_t1 = pd.read_csv('/Users/moose/Documents/MSTAR_Code/MSTAR/freezing_chamber/freezing_data/NaCaMg_25%_20%_15%_10%_5%/logs 10-24-2025-Fri 17-25-07-PM/ temps 10-24-2025-Fri 17-25-07-PM.csv')

# Add suffixes to avoid initial collisions
df_p1 = df_p1.add_suffix("_p1")
df_p2 = df_p2.add_suffix("_p2")
df_t1 = df_t1.add_suffix("_t1")

# -------------------- CONCENTRATIONS --------------------
# CHANGE THESE VARIABLES TO MATCH CELL CONCENTRATIONS
c1conc = "25pct";  c2conc = "25pct";  c3conc = "25pct";  c4conc = "25pct"
c5conc = "20pct";  c6conc = "20pct";  c7conc = "20pct";  c8conc = "20pct"
c9conc = "15pct"; c10conc = "15pct"; c11conc = "10pct"; c12conc = "10pct"
c13conc = "5pct"; c14conc = "5pct"; c15conc = "5pct"; c16conc = "5pct"

c1voltage  = f'{c1conc} Cell 1 Voltage'
c2voltage  = f'{c2conc} Cell 2 Voltage'
c3voltage  = f'{c3conc} Cell 3 Voltage'
c4voltage  = f'{c4conc} Cell 4 Voltage'
c5voltage  = f'{c5conc} Cell 5 Voltage'
c6voltage  = f'{c6conc} Cell 6 Voltage'
c7voltage  = f'{c7conc} Cell 7 Voltage'
c8voltage  = f'{c8conc} Cell 8 Voltage'
c9voltage  = f'{c9conc} Cell 9 Voltage'
c10voltage = f'{c10conc} Cell 10 Voltage'
c11voltage = f'{c11conc} Cell 11 Voltage'
c12voltage = f'{c12conc} Cell 12 Voltage'
c13voltage = f'{c13conc} Cell 13 Voltage'
c14voltage = f'{c14conc} Cell 14 Voltage'
c15voltage = f'{c15conc} Cell 15 Voltage'
c16voltage = f'{c16conc} Cell 16 Voltage'

c1current  = f'{c1conc} Cell 1 Current'
c2current  = f'{c2conc} Cell 2 Current'
c3current  = f'{c3conc} Cell 3 Current'
c4current  = f'{c4conc} Cell 4 Current'
c5current  = f'{c5conc} Cell 5 Current'
c6current  = f'{c6conc} Cell 6 Current'
c7current  = f'{c7conc} Cell 7 Current'
c8current  = f'{c8conc} Cell 8 Current'
c9current  = f'{c9conc} Cell 9 Current'
c10current = f'{c10conc} Cell 10 Current'
c11current = f'{c11conc} Cell 11 Current'
c12current = f'{c12conc} Cell 12 Current'
c13current = f'{c13conc} Cell 13 Current'
c14current = f'{c14conc} Cell 14 Current'
c15current = f'{c15conc} Cell 15 Current'
c16current = f'{c16conc} Cell 16 Current'

ts1  = f'{c2conc} Cell 2 Temp'
ts2  = f'{c4conc} Cell 4 Temp'
ts3  = f'{c6conc} Cell 6 Temp'
ts4  = f'{c8conc} Cell 8 Temp'
ts5  = f'{c9conc} Cell 9 Temp'
ts6  = f'{c11conc} Cell 11 Temp'
ts7  = f'{c13conc} Cell 13 Temp'
ts8  = f'{c15conc} Cell 15 Temp'

c1temp  = f'{c1conc} Cell 1 Temp'
c2temp  = ts1
c3temp  = f'{c3conc} Cell 3 Temp'
c4temp  = ts2
c5temp  = f'{c5conc} Cell 5 Temp'
c6temp  = ts3
c7temp  = f'{c7conc} Cell 7 Temp'
c8temp  = ts4
c9temp  = ts5
c10temp = f'{c10conc} Cell 10 Temp'
c11temp = ts6
c12temp = f'{c12conc} Cell 12 Temp'
c13temp = ts7
c14temp = f'{c14conc} Cell 14 Temp'
c15temp = ts8
c16temp = f'{c16conc} Cell 16 Temp'

c1resistance  = f'{c1conc} Cell 1 Resistance'
c2resistance  = f'{c2conc} Cell 2 Resistance'
c3resistance  = f'{c3conc} Cell 3 Resistance'
c4resistance  = f'{c4conc} Cell 4 Resistance'
c5resistance  = f'{c5conc} Cell 5 Resistance'
c6resistance  = f'{c6conc} Cell 6 Resistance'
c7resistance  = f'{c7conc} Cell 7 Resistance'
c8resistance  = f'{c8conc} Cell 8 Resistance'
c9resistance  = f'{c9conc} Cell 9 Resistance'
c10resistance = f'{c10conc} Cell 10 Resistance'
c11resistance = f'{c11conc} Cell 11 Resistance'
c12resistance = f'{c12conc} Cell 12 Resistance'
c13resistance = f'{c13conc} Cell 13 Resistance'
c14resistance = f'{c14conc} Cell 14 Resistance'
c15resistance = f'{c15conc} Cell 15 Resistance'
c16resistance = f'{c16conc} Cell 16 Resistance'

# -------------------- RENAME COLUMNS --------------------
# Map p1 channels
df_p1 = df_p1.rename(columns={
    "Timestamp_p1": "Timestamp",
    "mA 1_p1": c1current,  "V1_p1": c1voltage,
    "mA 2_p1": c2current,  "V2_p1": c2voltage,
    "mA 3_p1": c3current,  "V3_p1": c3voltage,
    "mA 4_p1": c4current,  "V4_p1": c4voltage,
    "mA 5_p1": c5current,  "V5_p1": c5voltage,
    "mA 6_p1": c6current,  "V6_p1": c6voltage,
    "mA 7_p1": c7current,  "V7_p1": c7voltage,
    "mA 8_p1": c8current,  "V8_p1": c8voltage,
})

# Map p2 channels
df_p2 = df_p2.rename(columns={
    "Timestamp_p2": "Timestamp",
    "mA 1_p2": c9current,  "V1_p2": c9voltage,
    "mA 2_p2": c10current, "V2_p2": c10voltage,
    "mA 3_p2": c11current, "V3_p2": c11voltage,
    "mA 4_p2": c12current, "V4_p2": c12voltage,
    "mA 5_p2": c13current, "V5_p2": c13voltage,
    "mA 6_p2": c14current, "V6_p2": c14voltage,
    "mA 7_p2": c15current, "V7_p2": c15voltage,
    "mA 8_p2": c16current, "V8_p2": c16voltage,
})

# Map T channels
df_t1 = df_t1.rename(columns={
    "Timestamp_t1": "Timestamp",
    "T1 - COM15_t1": f"{ts1}",
    "T2 - COM15_t1": f"{ts2}",
    "T3 - COM18_t1": f"{ts3}",
    "T4 - COM18_t1": f"{ts4}",
    "T5 - COM16_t1": f"{ts5}",
    "T6 - COM16_t1": f"{ts6}",
    "T7 - COM14_t1": f"{ts7}",
    "T8 - COM14_t1": f"{ts8}",
})

# -------------------- TYPE COERCION (NUMERIC) --------------------
# Convert numeric columns except Timestamp to numeric, coercing errors
for _df in (df_p1, df_p2, df_t1):
    num_cols = _df.columns.difference(['Timestamp'])
    _df[num_cols] = _df[num_cols].apply(pd.to_numeric, errors="coerce")

# -------------------- AVERAGED TEMPS (df_t2) --------------------
# Define which cell temperatures to average together at each timestamp
# Keys = new averaged column names; Values = list of temperature columns (from df_t1) to average
average_map = {  # HARDCODED, CHANGE TO MATCH EXPERIMENT
    f"{c1conc} Cell 1 Temp": [ts1, ts5],
    f"{c3conc} Cell 3 Temp": [ts1, ts2, ts6],
    f"{c5conc} Cell 5 Temp": [ts2, ts3, ts7],
    f"{c7conc} Cell 7 Temp": [ts3, ts4, ts8],
    f"{c10conc} Cell 10 Temp": [ts5, ts6, ts1],
    f"{c12conc} Cell 12 Temp": [ts6, ts7, ts2],
    f"{c14conc} Cell 14 Temp": [ts7, ts8, ts3],
    f"{c16conc} Cell 16 Temp": [ts8, ts4],
}

# Build df_t2 on df_p1's Timestamp (will be realigned later in a merge)
df_t2 = pd.DataFrame()
df_t2["Timestamp"] = df_p1["Timestamp"].copy()

for avg_name, cols in average_map.items():
    valid_cols = [c for c in cols if c in df_t1.columns]
    if not valid_cols:
        print(f"[WARNING] Skipping {avg_name} (no valid columns found)")
        continue
    df_t2[avg_name] = df_t1[valid_cols].mean(axis=1, skipna=True)

df_t2 = df_t2.round(3)
df_t2.to_csv(f"{experiment_name}_temps_averaged_by_time_{timestamp}.csv", index=False)

# -------------------- ALIGN ON TIME (CRITICAL FIX) --------------------
# Normalize timestamps and sort; then merge on time with tolerance
fmt = "%m-%d-%Y-%a %H-%M-%S-%p"
for name, _df in (("p1", df_p1), ("p2", df_p2), ("t1", df_t1), ("t2", df_t2)):
    _df["Timestamp"] = pd.to_datetime(_df["Timestamp"], format=fmt, errors="coerce")
    _df.sort_values("Timestamp", inplace=True)
    _df.reset_index(drop=True, inplace=True)

# Time-aware merges (not index concat)
tol = pd.Timedelta("1s")  # adjust for logger jitter, if needed
merged = pd.merge_asof(df_p1, df_p2, on="Timestamp", direction="nearest", tolerance=tol)
merged = pd.merge_asof(merged.sort_values("Timestamp"), df_t1.sort_values("Timestamp"),
                       on="Timestamp", direction="nearest", tolerance=tol)
merged = merged.merge(df_t2, on="Timestamp", how="left")

# Coerce numerics after merging
num_cols_all = merged.columns.difference(["Timestamp"])
merged[num_cols_all] = merged[num_cols_all].apply(pd.to_numeric, errors="coerce")

# Sanity checks (optional, can comment out)
assert merged["Timestamp"].is_monotonic_increasing
assert not merged["Timestamp"].isna().any()

# -------------------- RESISTANCE FOR ALL CELLS --------------------
# Calculate resistance: (V/I) * 0.00125, where I is in mA (convert by /1000 to A)
for i in range(1, 17):
    current_col = globals()[f'c{i}current']
    voltage_col = globals()[f'c{i}voltage']
    resistance_col = globals()[f'c{i}resistance']
    if current_col in merged.columns and voltage_col in merged.columns:
        merged[resistance_col] = (merged[voltage_col] / (merged[current_col] / 1000.0)) * 0.00125

# -------------------- OPTIONAL GLOBAL FILTERS --------------------
# If you truly want a global power-on window, do it fairly across boards:
voltage_cols_p1 = [c for c in merged.columns if "Voltage" in c and any(f"Cell {k} " in c for k in range(1, 9))]
voltage_cols_p2 = [c for c in merged.columns if "Voltage" in c and any(f"Cell {k} " in c for k in range(9, 17))]

mask_p1 = merged[voltage_cols_p1].ge(5).all(axis=1) if voltage_cols_p1 else True
mask_p2 = merged[voltage_cols_p2].ge(5).all(axis=1) if voltage_cols_p2 else True
mask_t  = merged[c1temp].lt(33) if c1temp in merged.columns else True

source = merged.loc[mask_p1 & mask_p2 & mask_t].copy()
# If you don't want any global gating, use: source = merged.copy()

# -------------------- ORDERED EXPORT (like your prior 'order') --------------------
order = [  # HARDCODED, CHANGE TO MATCH EXPERIMENT
    'Timestamp',
    c1current, c1voltage, c1resistance, c1temp,
    c2current, c2voltage, c2resistance, c2temp,
    c3current, c3voltage, c3resistance, c3temp,
    c4current, c4voltage, c4resistance, c4temp,
    c5current, c5voltage, c5resistance, c5temp,
    c6current, c6voltage, c6resistance, c6temp,
    c7current, c7voltage, c7resistance, c7temp,
    c8current, c8voltage, c8resistance, c8temp,
    c9current, c9voltage, c9resistance, c9temp,
    c10current, c10voltage, c10resistance, c10temp,
    c11current, c11voltage, c11resistance, c11temp,
    c12current, c12voltage, c12resistance, c12temp,
    c13current, c13voltage, c13resistance, c13temp,
    c14current, c14voltage, c14resistance, c14temp,
    c15current, c15voltage, c15resistance, c15temp,
    c16current, c16voltage, c16resistance, c16temp
]
order = [c for c in order if c in source.columns]  # guard if any missing

combined_data_ordered = source[order].copy()
combined_data_ordered.to_csv(f'{experiment_name}combined_data_{timestamp}.csv', index=False)

# -------------------- SAFE TRIMMER (POSITION-BASED) --------------------
def trim_after_current_drop(df, current_col, timestamp_col="Timestamp", threshold=0.1):
    """
    Sort by time, find the first row where current <= threshold (mA), and keep that and everything after.
    Uses position-based slicing to avoid index-label pitfalls.
    """
    df = df.sort_values(timestamp_col).reset_index(drop=True)
    s = pd.to_numeric(df[current_col], errors="coerce")
    mask = s <= threshold
    if not mask.any():
        return df.iloc[0:0].copy()
    first_pos = int(np.argmax(mask.to_numpy()))
    return df.iloc[first_pos:].copy()

# -------------------- PER-CELL TRIMMING & CONCAT --------------------
cell_dfs = []
for i in range(1, 17):
    curr_col = globals()[f'c{i}current']
    volt_col = globals()[f'c{i}voltage']
    temp_col = globals()[f'c{i}temp']
    timestamp_col = "Timestamp"

    # Skip cells missing columns
    missing_cols = [c for c in [timestamp_col, curr_col, volt_col, temp_col] if c not in source.columns]
    if missing_cols:
        print(f"[WARNING] Skipping Cell {i}: missing {missing_cols}")
        continue

    # Slice the per-cell view
    cell_df = source[[timestamp_col, curr_col, volt_col, temp_col]].copy()

    # Per-cell resistance (with volume correction)
    resistance_col = f'Cell {i} Resistance'
    cell_df[resistance_col] = (cell_df[volt_col] / (cell_df[curr_col] / 1000.0)) * 0.00125

    # Trim at first current <= threshold
    trimmed_df = trim_after_current_drop(cell_df, curr_col, timestamp_col, threshold=0.1)

    # Append with per-cell timestamp name to avoid collisions on concat
    if not trimmed_df.empty:
        trimmed_df = trimmed_df.rename(columns={timestamp_col: f"Cell {i} Timestamp"})
        cell_dfs.append(trimmed_df)
    else:
        empty_cols = [f"Cell {i} Timestamp", curr_col, volt_col, temp_col, resistance_col]
        cell_dfs.append(pd.DataFrame(columns=empty_cols))

# Concatenate side-by-side (index aligned, but each per-cell frame starts at its own drop)
analyzed_data = pd.concat(cell_dfs, axis=1).round(4)
analyzed_data.to_csv(f"{experiment_name}_analyzed_data_{timestamp}.csv", index=False)
print(f"✅ Saved analyzed data to {experiment_name}_analyzed_data_{timestamp}.csv")

# -------------------- DONE --------------------
print("✅ Temperature analysis complete.")