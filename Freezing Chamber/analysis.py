import csv
import pandas
import pandas as pd #Allows for data manipulation 
import numpy as np 
import time
from pathlib import Path 
import os 
from datetime import datetime

timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')

df_p1 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ power 1 09-27-2025-Sat 11-54-29-AM.csv') 
df_p2 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ power 2 09-27-2025-Sat 11-54-29-AM.csv') 
df_t1 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ temps 09-27-2025-Sat 11-54-29-AM.csv') 

df_p1 = df_p1.add_suffix("_p1")
df_p2 = df_p2.add_suffix("_p2")
df_t1 = df_t1.add_suffix("_t1")

df_p2 = df_p2.drop('Timestamp_p2', axis=1)
df_t1 = df_t1.drop('Timestamp_t1', axis=1)

ts1 = 'Cell 2'
ts2 = 'Cell 4'
ts3 = 'Cell6'
ts4 = 'Cell8'
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

#df_p1 = df_p1.columns = ['Timestamp', 'Cell 1 Current', 'Cell 1 Voltage', 'Cell 2 Current', 'Cell 2 Voltage', 'Cell 3 Current', 'Cell 3 Voltage', 'Cell 4 Current', 'Cell 4 Voltage', 'Cell 5 Current', 'Cell 5 Voltage', 'Cell 6 Current', 'Cell 6 Voltage', 'Cell 7 Current', 'Cell 7 Voltage', 'Cell 8 Current', 'Cell 8 Voltage']
#df_p2 = df_p2.columns = ['Cell 9 Current', 'Cell 9 Voltage', 'Cell 10 Current', 'Cell 10 Voltage', 'Cell 11 Current', 'Cell 11 Voltage', 'Cell 12 Current', 'Cell 12 Voltage', 'Cell 13 Current', 'Cell 13 Voltage', 'Cell 14 Current', 'Cell 14 Voltage', 'Cell 15 Current', 'Cell 15 Voltage', 'Cell 16 Current', 'Cell 16 Voltage']
#df_t1 = df_t1.columns = [f"{ts1} Temp", f"{ts2} Temp", f"{ts3} Temp", f"{ts4} Temp", f"{ts5} Temp", f"{ts6} Temp", f"{ts7} Temp", f"{ts8} Temp"]

#stating this variable off the columns.difference basically just applies this numeric to everything but the timestamp
num_cols_p1 = df_p1.columns.difference(['Timestamp'])
df_p1[num_cols_p1] = df_p1[num_cols_p1].apply(pd.to_numeric, errors="coerce")
num_cols_p2 = df_p2.columns.difference(['Timestamp_p2'])
df_p2[num_cols_p2] = df_p2[num_cols_p2].apply(pd.to_numeric, errors="coerce")
num_cols_t1 = df_t1.columns.difference(['Timestamp_t1'])
df_t1[num_cols_t1] = df_t1[num_cols_t1].apply(pd.to_numeric, errors="coerce")

#df_p1 = df_p1.apply(pd.to_numeric, errors="coerce") 
#df_p2 = df_p2.apply(pd.to_numeric, errors="coerce") 
#df_t1 = df_t1.apply(pd.to_numeric, errors="coerce") 


#combined_data = df[(df['mA 1'] <= .1) & (df['V1'] > 5)] #Filters the data to only take values when mA 1 is less than .1 and V1 is more than 5 
 
power_data_p1 = df_p1[(df_p1['Cell 1 Voltage'] > -5)] 
power_data_p2 = df_p2[(df_p2['Cell 9 Voltage'] > -5)]  
temp_data_t1 = df_t1[(df_t1[f'{ts1} Temp'] < 33)] 

combined_data = pd.concat([power_data_p1, power_data_p2, temp_data_t1], axis=1) 

order = [
    'Timestamp',
    'Cell 1 Current',
    'Cell 1 Voltage',
    'Cell 2 Current',
    'Cell 2 Voltage',
    f"{ts1} Temp",
    'Cell 3 Current',
    'Cell 3 Voltage',
    'Cell 4 Current',
    'Cell 4 Voltage',
    f"{ts2} Temp",
    'Cell 5 Current',
    'Cell 5 Voltage',
    'Cell 6 Current',
    'Cell 6 Voltage',
    f"{ts3} Temp",
    'Cell 7 Current',
    'Cell 7 Voltage',
    'Cell 8 Current',
    'Cell 8 Voltage',
    f"{ts4} Temp",  
    'Cell 9 Current',
    'Cell 9 Voltage',
    f"{ts5} Temp",
    'Cell 10 Current',
    'Cell 10 Voltage',
    'Cell 11 Current',
    'Cell 11 Voltage',
    f"{ts6} Temp",
    'Cell 12 Current',
    'Cell 12 Voltage',
    'Cell 13 Current',
    'Cell 13 Voltage',
    f"{ts7} Temp",
    'Cell 14 Current',
    'Cell 14 Voltage',
    'Cell 15 Current',
    'Cell 15 Voltage',
    f"{ts8} Temp",
    'Cell 16 Current',
    'Cell 16 Voltage',

]

combined_data_ordered = combined_data[order]

combined_data_ordered.to_csv(f'combined_data_{timestamp}.csv', index=False)

#combined_data.to_csv(f'combined_data.csv_{timestamp}', index=False) #index=False removes the labing index that is to the left of the data by default e.g. 1,2,3,4,5,6,7,...,n


#Everything above this line organaizes the data and filters it based on the conditions set
#Everything below this line is for analysis of the data

power_on_data = combined_data_ordered[(combined_data_ordered['Cell 1 Voltage'] > 5)] 

power_on_data.to_csv(f'power_on_data_{timestamp}.csv', index=False)