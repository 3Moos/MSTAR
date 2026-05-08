import csv
import pandas
import pandas as pd #Allows for data manipulation 
import numpy as np 
import time
from pathlib import Path 
import os 
from datetime import datetime

#Make sure to change hardcoded flie names before running script
#Make sure to change hard coded values of the Temp Sensors "ts1, ts2, etc." to match the actual sensor to cell used in the experiment
#Make sure to change the hardcdoded values in the average_map dictionary to match the actual cell numbers and average cells used for extrapolation
#Also Change the Hardcoded order list to match the actual sensor to cell used in the experiment
#Make sure to chamge the hardcoded experiment name in variable below
#32 #CHNAGE THESE VARIABLES TO MAGTCH CELL CONC

experiment_name = "x57-x60" #CHANGE THIS TO MATCH EXPERIMENT, USED IN OUTPUT FILE NAMES

timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')

df_p1 = pd.DataFrame()
df_p2 = pd.DataFrame()
df_t1 = pd.DataFrame()

# Hardcoded folder path (change this to match your experiment folder)
folder_path = "/Users/moose/Desktop/MSTAR/freezing_chamber/freezing_data/x57-60"

if not os.path.isdir(folder_path):
    raise FileNotFoundError(f"Folder not found: {folder_path}")

files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

power1_file = next(
    (f for f in files
     if any(sub in f.lower() for sub in ("power_1", "power 1")) and f.lower().endswith(".csv")),
    None
)
power2_file = next(
    (f for f in files
     if any(sub in f.lower() for sub in ("power_2", "power 2")) and f.lower().endswith(".csv")),
    None
)
temp_file = next(
    (f for f in files
     if any(sub in f.lower() for sub in ("temps", "temp")) and f.lower().endswith(".csv")),
    None
)

if not (power1_file and power2_file and temp_file):
    missing = []
    if not power1_file:
        missing.append("power 1")
    if not power2_file:
        missing.append("power 2")
    if not temp_file:
        missing.append("temp")
    raise FileNotFoundError(f"Missing file(s) in {folder_path}: {', '.join(missing)}")

try:
    if power1_file:
        df_p1 = pd.read_csv(os.path.join(folder_path, power1_file))
    else:
        print("[ERROR] No 'power 1' file found in folder")
    
    if power2_file:
        df_p2 = pd.read_csv(os.path.join(folder_path, power2_file))
    else:
        print("[ERROR] No 'power 2' file found in folder")
    
    if temp_file:
        df_t1 = pd.read_csv(os.path.join(folder_path, temp_file))
    else:
        print("[ERROR] No 'temp' file found in folder")
except Exception as e:
    print(f"[ERROR] Failed to load dataframes: {e}")
finally:
    print("✅ Loaded dataframes (check for errors above)")

#End of the file loading coke



df_p1 = df_p1.add_suffix("_p1")
df_p2 = df_p2.add_suffix("_p2")
df_t1 = df_t1.add_suffix("_t1")

#Drop the timestamps from t1 and p2 and just use the timestamp from p1 to avoid duplicate timestamp columns when concatenating later. This is because the timestamps should be the same across all files, so we only need one.
if 'Timestamp_p2' in df_p2.columns:
    df_p2 = df_p2.drop('Timestamp_p2', axis=1)
if 'Timestamp_t1' in df_t1.columns:
    df_t1 = df_t1.drop('Timestamp_t1', axis=1)

#CHNAGE THESE VARIABLES TO MAGTCH CELL CONC
c1conc = "x57"
c2conc = "x57"
c3conc = "x57"
c4conc = "x57"
c5conc = "x58"
c6conc = "x58"
c7conc = "x58"
c8conc = "x58"
c9conc = "x59"
c10conc = "x59"
c11conc = "x59"
c12conc = "x59"
c13conc = "x60"
c14conc = "x60"
c15conc = "x60"
c16conc = "x60"

c1voltage = f'{c1conc} Cell 1 Voltage'
c2voltage = f'{c2conc} Cell 2 Voltage'
c3voltage = f'{c3conc} Cell 3 Voltage'
c4voltage = f'{c4conc} Cell 4 Voltage'
c5voltage = f'{c5conc} Cell 5 Voltage'
c6voltage = f'{c6conc} Cell 6 Voltage'
c7voltage = f'{c7conc} Cell 7 Voltage'
c8voltage = f'{c8conc} Cell 8 Voltage'
c9voltage = f'{c9conc} Cell 9 Voltage'
c10voltage = f'{c10conc} Cell 10 Voltage'
c11voltage = f'{c11conc} Cell 11 Voltage'
c12voltage = f'{c12conc} Cell 12 Voltage'
c13voltage = f'{c13conc} Cell 13 Voltage'
c14voltage = f'{c14conc} Cell 14 Voltage'
c15voltage = f'{c15conc} Cell 15 Voltage'
c16voltage = f'{c16conc} Cell 16 Voltage'

c1current = f'{c1conc} Cell 1 Current'
c2current = f'{c2conc} Cell 2 Current'
c3current = f'{c3conc} Cell 3 Current'
c4current = f'{c4conc} Cell 4 Current'
c5current = f'{c5conc} Cell 5 Current'
c6current = f'{c6conc} Cell 6 Current'
c7current = f'{c7conc} Cell 7 Current'
c8current = f'{c8conc} Cell 8 Current'
c9current = f'{c9conc} Cell 9 Current'
c10current = f'{c10conc} Cell 10 Current'
c11current = f'{c11conc} Cell 11 Current'
c12current = f'{c12conc} Cell 12 Current'
c13current = f'{c13conc} Cell 13 Current'
c14current = f'{c14conc} Cell 14 Current'
c15current = f'{c15conc} Cell 15 Current'
c16current = f'{c16conc} Cell 16 Current'

ts1 = f'{c1conc} Cell 1 Temp'
ts2 = f'{c4conc} Cell 4 Temp'
ts3 = f'{c7conc} Cell 7 Temp'
ts4 = f'{c10conc} Cell 10 Temp'
ts5 = f'{c14conc} Cell 14 Temp'
ts6 = f'{c16conc} Cell 16 Temp'


c1temp = f'{c1conc} Cell 1 Temp'
c2temp = f'{c2conc} Cell 2 Temp'
c3temp = f'{c3conc} Cell 3 Temp'
c4temp = f'{c4conc} Cell 4 Temp'
c5temp = f'{c5conc} Cell 5 Temp'
c6temp = f'{c6conc} Cell 6 Temp'
c7temp = f'{c7conc} Cell 7 Temp'
c8temp = f'{c8conc} Cell 8 Temp'
c9temp = f'{c9conc} Cell 9 Temp'
c10temp = f'{c10conc} Cell 10 Temp'
c11temp = f'{c11conc} Cell 11 Temp'
c12temp = f'{c12conc} Cell 12 Temp'
c13temp = f'{c13conc} Cell 13 Temp'
c14temp = f'{c14conc} Cell 14 Temp'
c15temp = f'{c15conc} Cell 15 Temp'
c16temp = f'{c16conc} Cell 16 Temp'

c1resistance = f'{c1conc} Cell 1 Resistance'
c2resistance = f'{c2conc} Cell 2 Resistance'
c3resistance = f'{c3conc} Cell 3 Resistance'
c4resistance = f'{c4conc} Cell 4 Resistance'
c5resistance = f'{c5conc} Cell 5 Resistance'
c6resistance = f'{c6conc} Cell 6 Resistance'
c7resistance = f'{c7conc} Cell 7 Resistance'
c8resistance = f'{c8conc} Cell 8 Resistance'
c9resistance = f'{c9conc} Cell 9 Resistance'
c10resistance = f'{c10conc} Cell 10 Resistance'
c11resistance = f'{c11conc} Cell 11 Resistance'
c12resistance = f'{c12conc} Cell 12 Resistance'
c13resistance = f'{c13conc} Cell 13 Resistance'
c14resistance = f'{c14conc} Cell 14 Resistance'
c15resistance = f'{c15conc} Cell 15 Resistance'
c16resistance = f'{c16conc} Cell 16 Resistance'



df_p1 = df_p1.rename(columns={
    "Timestamp_p1" : "Timestamp",
    "mA 1_p1" : c1current,
    "V1_p1" : c1voltage,
    "mA 2_p1" : c2current,
    "V2_p1" : c2voltage,
    "mA 3_p1" : c3current,
    "V3_p1" : c3voltage,
    "mA 4_p1" : c4current,
    "V4_p1" : c4voltage,
    "mA 5_p1" : c5current,
    "V5_p1" : c5voltage,
    "mA 6_p1" : c6current,
    "V6_p1" : c6voltage,
    "mA 7_p1" : c7current,
    "V7_p1" : c7voltage,
    "mA 8_p1" : c8current,
    "V8_p1" : c8voltage,
}
                     )

df_p2 = df_p2.rename(columns={
    "mA 1_p2" : c9current,
    "V1_p2" : c9voltage,
    "mA 2_p2" : c10current,
    "V2_p2" : c10voltage,
    "mA 3_p2" : c11current,
    "V3_p2" : c11voltage,
    "mA 4_p2" : c12current,
    "V4_p2" : c12voltage,
    "mA 5_p2" : c13current,
    "V5_p2" : c13voltage,
    "mA 6_p2" : c14current,
    "V6_p2" : c14voltage,
    "mA 7_p2" : c15current,
    "V7_p2" : c15voltage,
    "mA 8_p2" : c16current,
    "V8_p2" : c16voltage,
}
                     )

   # Don't think to hard about the actual names here, just make sure the match the column headers on the temp file.
   # these lines just say take the columns from df_t1 and rename the column in quotes to another name in quotes
df_t1 = df_t1.rename(columns={
    f"T1 - COM14" : f"{ts1}",
    f"T2 - COM4" : f"{ts2}",
    f"T3 - COM6" : f"{ts3}",
    f"T4 - COMM18" : f"{ts4}",
    f"T5 - COMM16" : f"{ts5}",
    f"T6 - COMM16" : f"{ts6}",
    #f"T7 - COMM14" : f"{ts7}",
    #f"T8 - COMM14" : f"{ts8}"
}
                     )

#stating this variable off the columns.difference basically just applies this numeric to everything but the timestamp
num_cols_p1 = df_p1.columns.difference(['Timestamp'])
df_p1[num_cols_p1] = df_p1[num_cols_p1].apply(pd.to_numeric, errors="coerce")
num_cols_p2 = df_p2.columns.difference(['Timestamp_p2'])
df_p2[num_cols_p2] = df_p2[num_cols_p2].apply(pd.to_numeric, errors="coerce")
num_cols_t1 = df_t1.columns.difference(['Timestamp_t1'])
df_t1[num_cols_t1] = df_t1[num_cols_t1].apply(pd.to_numeric, errors="coerce")


#Extrapolated Temp Data

# Define which cell temperatures to average together at each timestamp
# Keys = new averaged column names
# Values = list of temperature columns in df_t1 to average
average_map = { #HARDCODED, CHANGE TO MATCH EXPERIMENT
    f"{c1conc} Cell 1 Temp": [ts1],
    f"{c2conc} Cell 2 Temp": [ts1, ts4,],
    f"{c3conc} Cell 3 Temp": [ts2, ts4],
    f"{c4conc} Cell 4 Temp": [ts2],
    f"{c5conc} Cell 5 Temp": [ts2, ts5],
    f"{c6conc} Cell 6 Temp": [ts5, ts3],
    f"{c7conc} Cell 7 Temp": [ts3],
    f"{c8conc} Cell 8 Temp": [ts3, ts6],
    f"{c9conc} Cell 9 Temp": [ts1, ts4],
    f"{c10conc} Cell 10 Temp": [ts4],
    f"{c11conc} Cell 11 Temp": [ts4, ts2],
    f"{c12conc} Cell 12 Temp": [ts2],
    f"{c13conc} Cell 13 Temp": [ts5, ],
    f"{c14conc} Cell 14 Temp": [ts1],
    f"{c15conc} Cell 15 Temp": [ts1],
    f"{c16conc} Cell 16 Temp": [ts1]
    }

# Create df_t2 with timestamps, so empty dataframe with just the timestamp column to start, then we will add the extrapolated temp columns to it
df_t2 = pd.DataFrame()
df_t2["Timestamp"] = df_p1["Timestamp"]

# Compute time-aligned averages
for avg_name, cols in average_map.items():
    valid_cols = [c for c in cols if c in df_t1.columns]
    if not valid_cols:
        print(f"[WARNING] Skipping {avg_name} (no valid columns found)")
        df_t2[avg_name] = np.nan
        continue
    df_t2[avg_name] = df_t1[valid_cols].mean(axis=1, skipna=True)

# round for readability
df_t2 = df_t2.round(3)

# Save output
df_t2.to_csv(f"{experiment_name}_temps_averaged_by_time_{timestamp}.csv", index=False)



#Calculating resistanc values


#df_p1 = df_p1.apply(pd.to_numeric, errors="coerce") 
#df_p2 = df_p2.apply(pd.to_numeric, errors="coerce") 
#df_t1 = df_t1.apply(pd.to_numeric, errors="coerce") 

#power_data_p1 = df_p1[(df_p1['Cell 1 Voltage'] > -5)] 
#power_data_p2 = df_p2[(df_p2['Cell 11 Voltage'] > -5)]  
#temp#power_data_p1 = df_p1[df_p1[[col for col in df_p1.columns if "Voltage" in col]].ge(5).all(axis=1)]
#temp#power_data_p2 = df_p2[df_p2[[col for col in df_p2.columns if "Voltage" in col]].ge(5).all(axis=1)]

#temp

# If df_p1 is blank, keep it as-is
if df_p1.empty:
    power_data_p1 = df_p1.copy()
else:
    voltage_cols_p1 = [col for col in df_p1.columns if "Voltage" in col]
    power_data_p1 = df_p1[df_p1[voltage_cols_p1].ge(5).all(axis=1)]

# Only apply voltage > 5 filter to df_p2
voltage_cols_p2 = [col for col in df_p2.columns if "Voltage" in col]
power_data_p2 = df_p2[df_p2[voltage_cols_p2].ge(5).all(axis=1)]

#temp


temp_data_t1 = df_t1[df_t1[ts1] < 33] if ts1 in df_t1.columns else df_t1.copy()  #HARDCODED VALUE, CHANGE TO MATCH EXPERIMENT
# Filter df_t2 by temperature but drop its Timestamp column to avoid duplicate Timestamp columns when concatenating
if 'Timestamp' in df_t2.columns:
    temp_data_t2 = df_t2[df_t2[f"{c1conc} Cell 1 Temp"] < 33].drop(columns=['Timestamp'])
else:
    temp_data_t2 = df_t2[df_t2[f"{c1conc} Cell 1 Temp"] < 33]

combined_data = pd.concat([power_data_p1, power_data_p2, temp_data_t1, temp_data_t2], axis=1) 

# Calculate resistance for all cells in combined_data
for i in range(1, 17):
    current_col = globals()[f'c{i}current']
    voltage_col = globals()[f'c{i}voltage']
    resistance_col = globals()[f'c{i}resistance']  # Use the concentration-prefixed column name
    if current_col in combined_data.columns and voltage_col in combined_data.columns:
        # Calculate resistance: (V/I) * volume_correction
        combined_data[resistance_col] = (combined_data[voltage_col] / (combined_data[current_col] / 1000)) * 0.00125

order = ['Timestamp']
for i in range(1, 17):
    for col_name in (
        globals()[f'c{i}current'],
        globals()[f'c{i}voltage'],
        globals()[f'c{i}resistance'],
        globals()[f'c{i}temp'],
    ):
        if col_name in combined_data.columns:
            order.append(col_name)

combined_data_ordered = combined_data[order]

combined_data_ordered.to_csv(f'{experiment_name}_combined_data_{timestamp}.csv', index=False)

if c9voltage in combined_data_ordered.columns:
    power_on_data = combined_data_ordered[combined_data_ordered[c9voltage] > 5]
else:
    power_on_data = combined_data_ordered.copy()

power_on_data.to_csv(f'{experiment_name}_power_on_data_{timestamp}.csv', index=False)

#Everything above this line organaizes the data and filters it based on the conditions set
#Everything below this line is for analysis of the data







def trim_after_current_drop(df, current_col, timestamp_col, threshold=0.2):
    """Find first row where current <= threshold and keep all rows after, preserving timestamps."""
    below_threshold = df[df[current_col] <= threshold]
    if below_threshold.empty:
        return pd.DataFrame(columns=df.columns)
    first_index = below_threshold.index[0]
    return df.loc[first_index:]  # keep that and everything after


cell_dfs = []
for i in range(1, 17):
    curr_col = globals()[f'c{i}current']
    volt_col = globals()[f'c{i}voltage']
    temp_col = globals()[f'c{i}temp']
    timestamp_col = "Timestamp"

    # Skip cells missing columns
    missing_cols = [c for c in [curr_col, volt_col, temp_col, timestamp_col] if c not in power_on_data.columns]
    if missing_cols:
        print(f"[WARNING] Skipping Cell {i}: missing {missing_cols}")
        continue

    # Include timestamp in the slice
    cell_df = power_on_data[[timestamp_col, curr_col, volt_col, temp_col]].copy()
    
    # Calculate resistance with volume correction (0.00125)
    resistance_col = f'Cell {i} Resistance'
    cell_df[resistance_col] = (cell_df[volt_col] / (cell_df[curr_col] / 1000)) * 0.00125

    # Get trimmed data with timestamps
    trimmed_df = trim_after_current_drop(cell_df, curr_col, timestamp_col)

    # If valid data exists, rename timestamp for this cell and append
    if not trimmed_df.empty:
        # rename and reset index so concatenation doesn't align on original dataframe indices
        trimmed_df = trimmed_df.rename(columns={timestamp_col: f"Cell {i} Timestamp"})
        trimmed_df = trimmed_df.reset_index(drop=True)
        # debug: report trimmed length and first timestamp
        try:
            first_ts = trimmed_df.iloc[0][f"Cell {i} Timestamp"]
        except Exception:
            first_ts = None
        print(f"Cell {i}: trimmed rows={len(trimmed_df)}, start_timestamp={first_ts}")
        cell_dfs.append(trimmed_df)
    else:
        # If no cutoff found, append empty df with same columns including renamed timestamp
        empty_cols = [f"Cell {i} Timestamp", curr_col, volt_col, temp_col, resistance_col]
        cell_dfs.append(pd.DataFrame(columns=empty_cols))

# --- Concatenate cells side-by-side ---
analyzed_data = pd.concat(cell_dfs, axis=1)

# Optional: round to clean decimals
analyzed_data = analyzed_data.round(4)

# Export
analyzed_data.to_csv(f"{experiment_name}_analyzed_data_{timestamp}.csv", index=False)
print(f"✅ Saved trimmed (index-aligned) data to {experiment_name}_analyzed_data_{timestamp}.csv")

#Vibe end