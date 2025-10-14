import pandas as pd
import numpy as np
from datetime import datetime
import os

# ================================
# ---- CONFIGURATION SECTION -----
# ================================

experiment_name = "CaNaMg, 35%, 30% - 9-5-2025"

# File paths (edit as needed)
df_p1_path = '/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/blank.csv'
df_p2_path = '/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ power 2 09-05-2025-Fri 16-34-30-PM.csv'
df_t1_path = '/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ temps 09-05-2025-Fri 16-34-30-PM.csv'

timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')

# ================================
# ---- LOAD AND PREP DATA --------
# ================================

df_p1 = pd.read_csv(df_p1_path)
df_p2 = pd.read_csv(df_p2_path)
df_t1 = pd.read_csv(df_t1_path)

df_p1 = df_p1.add_suffix("_p1")
df_p2 = df_p2.add_suffix("_p2")
df_t1 = df_t1.add_suffix("_t1")

# Drop timestamp suffix cols that duplicate
for df, col in [(df_p1, 'Timestamp_p1'), (df_p2, 'Timestamp_p2'), (df_t1, 'Timestamp_t1')]:
    if col in df.columns:
        df.drop(columns=[col], inplace=True)

# Sensor to cell mapping
ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8 = 'Cell 2', 'Cell 4', 'Cell 6', 'Cell 8', 'Cell 9', 'Cell 11', 'Cell 13', 'Cell 15'

# Rename columns for power data
df_p1 = df_p1.rename(columns={
    "mA 1_p1": "Cell 1 Current", "V1_p1": "Cell 1 Voltage",
    "mA 2_p1": "Cell 2 Current", "V2_p1": "Cell 2 Voltage",
    "mA 3_p1": "Cell 3 Current", "V3_p1": "Cell 3 Voltage",
    "mA 4_p1": "Cell 4 Current", "V4_p1": "Cell 4 Voltage",
    "mA 5_p1": "Cell 5 Current", "V5_p1": "Cell 5 Voltage",
    "mA 6_p1": "Cell 6 Current", "V6_p1": "Cell 6 Voltage",
    "mA 7_p1": "Cell 7 Current", "V7_p1": "Cell 7 Voltage",
    "mA 8_p1": "Cell 8 Current", "V8_p1": "Cell 8 Voltage"
})

df_p2 = df_p2.rename(columns={
    "mA 1_p2": "Cell 9 Current", "V1_p2": "Cell 9 Voltage",
    "mA 2_p2": "Cell 10 Current", "V2_p2": "Cell 10 Voltage",
    "mA 3_p2": "Cell 11 Current", "V3_p2": "Cell 11 Voltage",
    "mA 4_p2": "Cell 12 Current", "V4_p2": "Cell 12 Voltage",
    "mA 5_p2": "Cell 13 Current", "V5_p2": "Cell 13 Voltage",
    "mA 6_p2": "Cell 14 Current", "V6_p2": "Cell 14 Voltage",
    "mA 7_p2": "Cell 15 Current", "V7_p2": "Cell 15 Voltage",
    "mA 8_p2": "Cell 16 Current", "V8_p2": "Cell 16 Voltage"
})

df_t1 = df_t1.rename(columns={
    f"T1 - COM15_t1": f"{ts1} Temp", f"T2 - COM15_t1": f"{ts2} Temp",
    f"T3 - COM18_t1": f"{ts3} Temp", f"T4 - COM18_t1": f"{ts4} Temp",
    f"T5 - COM16_t1": f"{ts5} Temp", f"T6 - COM16_t1": f"{ts6} Temp",
    f"T7 - COM14_t1": f"{ts7} Temp", f"T8 - COM14_t1": f"{ts8} Temp"
})

# ================================
# ---- CLEAN / CONVERT NUMERIC ----
# ================================

for df in [df_p1, df_p2, df_t1]:
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ================================
# ---- AVERAGE TEMP CALCULATION ---
# ================================

average_map = {
    "Cell 1 Temp": ["Cell 2 Temp", "Cell 9 Temp"],
    "Cell 3 Temp": ["Cell 2 Temp", "Cell 4 Temp", "Cell 11 Temp"],
    "Cell 5 Temp": ["Cell 4 Temp", "Cell 6 Temp", "Cell 13 Temp"],
    "Cell 7 Temp": ["Cell 6 Temp", "Cell 8 Temp", "Cell 15 Temp"],
    "Cell 10 Temp": ["Cell 9 Temp", "Cell 11 Temp", "Cell 2 Temp"],
    "Cell 12 Temp": ["Cell 11 Temp", "Cell 13 Temp", "Cell 4 Temp"],
    "Cell 14 Temp": ["Cell 13 Temp", "Cell 15 Temp", "Cell 6 Temp"],
    "Cell 16 Temp": ["Cell 15 Temp", "Cell 8 Temp"]
}

df_t2 = pd.DataFrame()
df_t2["Timestamp"] = df_t1.index.astype(str)
for avg_name, cols in average_map.items():
    valid_cols = [c for c in cols if c in df_t1.columns]
    df_t2[avg_name] = df_t1[valid_cols].mean(axis=1, skipna=True)
df_t2 = df_t2.round(3)
df_t2.to_csv(f"{experiment_name}_temps_averaged_by_time_{timestamp}.csv", index=False)

# ================================
# ---- FILTERING / MERGING -------
# ================================

# Voltage filtering (only for df_p2)
voltage_cols_p2 = [c for c in df_p2.columns if "Voltage" in c]
power_data_p1 = df_p1.copy()  # blank = stays blank
power_data_p2 = df_p2[df_p2[voltage_cols_p2].ge(5).all(axis=1)]

# Temperature filters
temp_data_t1 = df_t1[df_t1[f"{ts1} Temp"] < 33]
temp_data_t2 = df_t2[df_t2["Cell 1 Temp"] < 33]

combined_data = pd.concat([power_data_p1, power_data_p2, temp_data_t1, temp_data_t2], axis=1)
combined_data.to_csv(f"{experiment_name}_combined_data_{timestamp}.csv", index=False)
print(f"✅ Combined data saved with {combined_data.shape[0]} rows and {combined_data.shape[1]} columns.")

power_on_data = combined_data[(combined_data.filter(like="Voltage") > 5).any(axis=1)]
power_on_data.to_csv(f"{experiment_name}_power_on_data_{timestamp}.csv", index=False)

# ================================
# ---- ANALYSIS PHASE ------------
# ================================

def trim_after_current_drop(df, current_col, threshold=0.1):
    """Find first row where current <= threshold and keep all rows after."""
    df[current_col] = pd.to_numeric(df[current_col], errors="coerce")
    below = df[df[current_col] <= threshold]
    if below.empty:
        return pd.DataFrame(columns=df.columns)
    first_idx = below.index[0]
    return df.loc[first_idx:]

cell_dfs = []
for i in range(1, 17):
    curr_col = f"Cell {i} Current"
    volt_col = f"Cell {i} Voltage"
    temp_col = f"Cell {i} Temp"

    if not all(c in power_on_data.columns for c in [curr_col, volt_col, temp_col]):
        print(f"[WARNING] Skipping Cell {i}: Missing columns")
        # Append empty dataframe for missing cells (to preserve structure)
        cell_dfs.append(pd.DataFrame(columns=[curr_col, volt_col, temp_col]))
        continue

    cell_df = power_on_data[[curr_col, volt_col, temp_col]].copy()
    trimmed_df = trim_after_current_drop(cell_df, curr_col)
    trimmed_df = trimmed_df.reset_index(drop=True)
    cell_dfs.append(trimmed_df)

analyzed_data = pd.concat(cell_dfs, axis=1).round(4)
analyzed_data.to_csv(f"{experiment_name}_analyzed_data_{timestamp}.csv", index=False)

print(f"✅ Saved analyzed data with {analyzed_data.shape[0]} rows and {analyzed_data.shape[1]} columns.")
