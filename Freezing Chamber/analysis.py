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

experiment_name = "CaNaMg, 35%, 30% - 9-5-2025"

timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')

df_p1 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/blank.csv') 
df_p2 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/blank.csv') 
df_t1 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ temps 09-05-2025-Fri 16-34-30-PM.csv') 


df_p1 = df_p1.add_suffix("_p1")
df_p2 = df_p2.add_suffix("_p2")
df_t1 = df_t1.add_suffix("_t1")

df_p2 = df_p2.drop('Timestamp_p2', axis=1)
df_t1 = df_t1.drop('Timestamp_t1', axis=1)

ts1 = 'Cell 2'
ts2 = 'Cell 4'
ts3 = 'Cell 6'
ts4 = 'Cell 8'
ts5 = 'Cell 9'
ts6 = 'Cell 11'
ts7 = 'Cell 13'
ts8 = 'Cell 15'

df_p1 = df_p1.rename(columns={
    "Timestamp_p1" : "Timestamp",
    "mA 1_p1" : "Cell 1 Current",
    "V1_p1" : "Cell 1 Voltage",
    "mA 2_p1" : "Cell 2 Current",
    "V2_p1" : "Cell 2 Voltage",
    "mA 3_p1" : "Cell 3 Current",
    "V3_p1" : "Cell 3 Voltage",
    "mA 4_p1" : "Cell 4 Current",
    "V4_p1" : "Cell 4 Voltage",
    "mA 5_p1" : "Cell 5 Current",
    "V5_p1" : "Cell 5 Voltage",
    "mA 6_p1" : "Cell 6 Current",
    "V6_p1" : "Cell 6 Voltage",
    "mA 7_p1" : "Cell 7 Current",
    "V7_p1" : "Cell 7 Voltage",
    "mA 8_p1" : "Cell 8 Current",
    "V8_p1" : "Cell 8 Voltage"
}
                     )

df_p2 = df_p2.rename(columns={
    "mA 1_p2" : "Cell 9 Current",
    "V1_p2" : "Cell 9 Voltage",
    "mA 2_p2" : "Cell 10 Current",
    "V2_p2" : "Cell 10 Voltage",
    "mA 3_p2" : "Cell 11 Current",
    "V3_p2" : "Cell 11 Voltage",
    "mA 4_p2" : "Cell 12 Current",
    "V4_p2" : "Cell 12 Voltage",
    "mA 5_p2" : "Cell 13 Current",
    "V5_p2" : "Cell 13 Voltage",
    "mA 6_p2" : "Cell 14 Current",
    "V6_p2" : "Cell 14 Voltage",
    "mA 7_p2" : "Cell 15 Current",
    "V7_p2" : "Cell 15 Voltage",
    "mA 8_p2" : "Cell 16 Current",
    "V8_p2" : "Cell 16 Voltage"
}
                     )

df_t1 = df_t1.rename(columns={
    f"T1 - COM15_t1" : f"{ts1} Temp",
    f"T2 - COM15_t1" : f"{ts2} Temp",
    f"T3 - COM18_t1" : f"{ts3} Temp",
    f"T4 - COM18_t1" : f"{ts4} Temp",
    f"T5 - COM16_t1" : f"{ts5} Temp",
    f"T6 - COM16_t1" : f"{ts6} Temp",
    f"T7 - COM14_t1" : f"{ts7} Temp",
    f"T8 - COM14_t1" : f"{ts8} Temp"
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
#Vibe Start

# Define which cell temperatures to average together at each timestamp
# Keys = new averaged column names
# Values = list of temperature columns in df_t1 to average
average_map = { #HARDCODED, CHANGE TO MATCH EXPERIMENT
    "Cell 1 Temp": ["Cell 2 Temp", "Cell 9 Temp"],
    "Cell 3 Temp": ["Cell 2 Temp", "Cell 4 Temp", "Cell 11 Temp"],
    "Cell 5 Temp": ["Cell 4 Temp", "Cell 6 Temp", "Cell 13 Temp"],
    "Cell 7 Temp": ["Cell 6 Temp", "Cell 8 Temp", "Cell 15 Temp"],
    "Cell 10 Temp": ["Cell 9 Temp", "Cell 11 Temp", "Cell 2 Temp"],
    "Cell 12 Temp": ["Cell 11 Temp", "Cell 13 Temp", "Cell 4 Temp"],
    "Cell 14 Temp": ["Cell 13 Temp", "Cell 15 Temp", "Cell 6 Temp"],
    "Cell 16 Temp": ["Cell 15 Temp", "Cell 8 Temp"],
}

# Create df_t2 with timestamps
df_t2 = pd.DataFrame()
df_t2["Timestamp"] = df_p1["Timestamp"]

# Compute time-aligned averages
for avg_name, cols in average_map.items():
    valid_cols = [c for c in cols if c in df_t1.columns]
    if not valid_cols:
        print(f"[WARNING] Skipping {avg_name} (no valid columns found)")
        continue
    df_t2[avg_name] = df_t1[valid_cols].mean(axis=1, skipna=True)

# Optional: round for readability
df_t2 = df_t2.round(3)

# Save output
df_t2.to_csv(f"{experiment_name}_temps_averaged_by_time_{timestamp}.csv", index=False)




#Vibe End



#df_p1 = df_p1.apply(pd.to_numeric, errors="coerce") 
#df_p2 = df_p2.apply(pd.to_numeric, errors="coerce") 
#df_t1 = df_t1.apply(pd.to_numeric, errors="coerce") 

#power_data_p1 = df_p1[(df_p1['Cell 1 Voltage'] > -5)] 
#power_data_p2 = df_p2[(df_p2['Cell 11 Voltage'] > -5)]  
power_data_p1 = df_p1[df_p1[[col for col in df_p1.columns if "Voltage" in col]].ge(5).all(axis=1)]
power_data_p2 = df_p2[df_p2[[col for col in df_p2.columns if "Voltage" in col]].ge(5).all(axis=1)]
temp_data_t1 = df_t1[(df_t1['Cell 2 Temp'] < 33)]  #HARDCODED VALUE, CHANGE TO MATCH EXPERIMENT
temp_data_t2 = df_t2[(df_t2['Cell 1 Temp'] < 33)] #HARDCODED VALUE, CHANGE TO MATCH EXPERIMENT

combined_data = pd.concat([power_data_p1, power_data_p2, temp_data_t1, temp_data_t2], axis=1) 

order = [ #HARDCODED, CHANGE TO MATCH EXPERIMENT
    'Timestamp',
    'Cell 1 Current',
    'Cell 1 Voltage',
    'Cell 1 Temp',
    'Cell 2 Current',
    'Cell 2 Voltage',
    'Cell 2 Temp',
    'Cell 3 Current',
    'Cell 3 Voltage',
    'Cell 3 Temp',
    'Cell 4 Current',
    'Cell 4 Voltage',
    'Cell 4 Temp',
    'Cell 5 Current',
    'Cell 5 Voltage',
    'Cell 5 Temp',
    'Cell 6 Current',
    'Cell 6 Voltage',
    'Cell 6 Temp',
    'Cell 7 Current',
    'Cell 7 Voltage',
    'Cell 7 Temp',
    'Cell 8 Current',
    'Cell 8 Voltage',
    'Cell 8 Temp', 
    'Cell 9 Current',
    'Cell 9 Voltage',
    'Cell 9 Temp',
    'Cell 10 Current',
    'Cell 10 Voltage',
    'Cell 10 Temp',
    'Cell 11 Current',
    'Cell 11 Voltage',
    'Cell 11 Temp',
    'Cell 12 Current',
    'Cell 12 Voltage',
    'Cell 12 Temp',
    'Cell 13 Current',
    'Cell 13 Voltage',
    'Cell 13 Temp',
    'Cell 14 Current',
    'Cell 14 Voltage',
    'Cell 14 Temp',
    'Cell 15 Current',
    'Cell 15 Voltage',
    'Cell 15 Temp',
    'Cell 16 Current',
    'Cell 16 Voltage',
    'Cell 16 Temp'

]

combined_data_ordered = combined_data[order]

combined_data_ordered.to_csv(f'{experiment_name}combined_data_{timestamp}.csv', index=False)

#combined_data.to_csv(f'combined_data.csv_{timestamp}', index=False) #index=False removes the labing index that is to the left of the data by default e.g. 1,2,3,4,5,6,7,...,n

power_on_data = combined_data_ordered[(combined_data_ordered['Cell 9 Voltage'] > 5)] 

power_on_data.to_csv(f'{experiment_name}power_on_data_{timestamp}.csv', index=False)

#Everything above this line organaizes the data and filters it based on the conditions set

#Everything below this line is for analysis of the data

#Okay I need to basically parse each induvidual set of columns(ignoring timestamp) and then output all the data set for the specified value of current I was looking for then repeat to all of the sets (16 total))\

#cell1_data = power_on_data[['Cell 1 Current', 'Cell 1 Voltage', 'Cell 1 Temp']]
#cell2_data = power_on_data[['Cell 2 Current', 'Cell 2 Voltage', 'Cell 2 Temp']]
#cell3_data = power_on_data[['Cell 3 Current', 'Cell 3 Voltage', 'Cell 3 Temp']]
#cell4_data = power_on_data[['Cell 4 Current', 'Cell 4 Voltage', 'Cell 4 Temp']] 
#cell5_data = power_on_data[['Cell 5 Current', 'Cell 5 Voltage', 'Cell 5 Temp']]
#cell6_data = power_on_data[['Cell 6 Current', 'Cell 6 Voltage', 'Cell 6 Temp']]
#cell7_data = power_on_data[['Cell 7 Current', 'Cell 7 Voltage', 'Cell 7 Temp']]
#cell8_data = power_on_data[['Cell 8 Current', 'Cell 8 Voltage', 'Cell 8 Temp']]
#cell9_data = power_on_data[['Cell 9 Current', 'Cell 9 Voltage', 'Cell 9 Temp']]
#cell10_data = power_on_data[['Cell 10 Current', 'Cell 10 Voltage', 'Cell 10 Temp']]
#ell11_data = power_on_data[['Cell 11 Current', 'Cell 11 Voltage', 'Cell 11 Temp']]
#cell12_data = power_on_data[['Cell 12 Current', 'Cell 12 Voltage', 'Cell 12 Temp']]
#cell13_data = power_on_data[['Cell 13 Current', 'Cell 13 Voltage', 'Cell 13 Temp']]
#cell14_data = power_on_data[['Cell 14 Current', 'Cell 14 Voltage', 'Cell 14 Temp']]
#cell15_data = power_on_data[['Cell 15 Current', 'Cell 15 Voltage', 'Cell 15 Temp']]
#cell16_data = power_on_data[['Cell 16 Current', 'Cell 16 Voltage', 'Cell 16 Temp']]



#cell1_data = cell1_data[(cell1_data['Cell 1 Current'] <= .1)]
#cell2_data = cell2_data[(cell2_data['Cell 2 Current'] <= .1)]
#cell3_data = cell3_data[(cell3_data['Cell 3 Current'] <= .1)]
##cell4_data = cell4_data[(cell4_data['Cell 4 Current'] <= .1)]
#cell5_data = cell5_data[(cell5_data['Cell 5 Current'] <= .1)]
#cell6_data = cell6_data[(cell6_data['Cell 6 Current'] <= .1)]
#cell7_data = cell7_data[(cell7_data['Cell 7 Current'] <= .1)]
#cell8_data = cell8_data[(cell8_data['Cell 8 Current'] <= .1)]
#cell9_data = cell9_data[(cell9_data['Cell 9 Current'] <= .1)]
#cell10_data = cell10_data[(cell10_data['Cell 10 Current'] <= .1)]
#cell11_data = cell11_data[(cell11_data['Cell 11 Current'] <= .1)]
#cell12_data = cell12_data[(cell12_data['Cell 12 Current'] <= .1)]
#cell13_data = cell13_data[(cell13_data['Cell 13 Current'] <= .1)]
#cell14_data = cell14_data[(cell14_data['Cell 14 Current'] <= .1)]
#cell15_data = cell15_data[(cell15_data['Cell 15 Current'] <= .1)]
#cell16_data = cell16_data[(cell16_data['Cell 16 Current'] <= .1)]

#analyized_data = pd.concat([cell1_data, cell2_data, cell3_data, cell4_data, cell5_data, cell6_data, cell7_data, cell8_data, cell9_data, cell10_data, cell11_data, cell12_data, cell13_data, cell14_data, cell15_data, cell16_data], axis=1)

#analyized_data.to_csv(f'{experiment_name}analyized_data_{timestamp}.csv', index=False)


#Vibe begin

def trim_after_current_drop(df, current_col, threshold=0.1):
    """Find first row where current <= threshold and keep all rows after."""
    below_threshold = df[df[current_col] <= threshold]
    if below_threshold.empty:
        return pd.DataFrame(columns=df.columns)
    first_index = below_threshold.index[0]
    return df.loc[first_index:]  # keep that and everything after


cell_dfs = []
for i in range(1, 17):
    curr_col = f"Cell {i} Current"
    volt_col = f"Cell {i} Voltage"
    temp_col = f"Cell {i} Temp"

    # Skip cells missing columns
    missing_cols = [c for c in [curr_col, volt_col, temp_col] if c not in power_on_data.columns]
    if missing_cols:
        print(f"[WARNING] Skipping Cell {i}: missing {missing_cols}")
        continue

    # Slice relevant data only (no timestamp)
    cell_df = power_on_data[[curr_col, volt_col, temp_col]].copy()
    trimmed_df = trim_after_current_drop(cell_df, curr_col)

    # If valid, reset index so concat aligns properly
    if not trimmed_df.empty:
        trimmed_df = trimmed_df.reset_index(drop=True)
        cell_dfs.append(trimmed_df)
    else:
        # If no cutoff found, append empty df with same columns
        cell_dfs.append(pd.DataFrame(columns=[curr_col, volt_col, temp_col]))

# --- Concatenate by index (side-by-side) ---
analyzed_data = pd.concat(cell_dfs, axis=1)

# Optional: round to clean decimals
analyzed_data = analyzed_data.round(4)

# Export
analyzed_data.to_csv(f"{experiment_name}_analyzed_data_{timestamp}.csv", index=False)
print(f"✅ Saved trimmed (index-aligned) data to {experiment_name}_analyzed_data_{timestamp}.csv")

#Vibe end