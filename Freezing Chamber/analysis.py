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

#stating this variable off the columns.difference basically just applies this numeric to everything but the timestamp
num_cols_p1 = df_p1.columns.difference(['Timestamp_p1'])
df_p1[num_cols_p1] = df_p1[num_cols_p1].apply(pd.to_numeric, errors="coerce")
num_cols_p2 = df_p2.columns.difference(['Timestamp_p2'])
df_p2[num_cols_p2] = df_p2[num_cols_p2].apply(pd.to_numeric, errors="coerce")
num_cols_t1 = df_t1.columns.difference(['Timestamp_t1'])
df_t1[num_cols_t1] = df_t1[num_cols_t1].apply(pd.to_numeric, errors="coerce")

#df_p1 = df_p1.apply(pd.to_numeric, errors="coerce") 
#df_p2 = df_p2.apply(pd.to_numeric, errors="coerce") 
#df_t1 = df_t1.apply(pd.to_numeric, errors="coerce") 


#combined_data = df[(df['mA 1'] <= .1) & (df['V1'] > 5)] #Filters the data to only take values when mA 1 is less than .1 and V1 is more than 5 
 
power_data_p1 = df_p1[(df_p1['V1_p1'] > -5)] 
power_data_p2 = df_p2[(df_p2['V1_p2'] > -5)]  
temp_data_t1 = df_t1[(df_t1['T1 - COM15_t1'] < 33)] 

combined_data = pd.concat([power_data_p1, power_data_p2, temp_data_t1], axis=1) 

order = [
    'Timestamp_p1',
    'mA 1_p1',
    'V1_p1',
    'mA 2_p1',
    'V2_p1',
    'T1 - COM15_t1',
    'mA 3_p1',
    'V3_p1',
    'mA 4_p1',
    'V4_p1',
    'T2 - COM15_t1',
    'mA 5_p1',
    'V5_p1',
    'mA 6_p1',
    'V6_p1',
    'T3 - COM18_t1',
    'mA 7_p1',
    'V7_p1',
    'V8_p1',
    'T4 - COM18_t1',
    'mA 1_p2',
    'V1_p2',
    'T5 - COM16_t1',
    'mA 2_p2',
    'V2_p2',
    'mA 3_p2',
    'V3_p2',
    'T6 - COM16_t1',
    'mA 4_p2',
    'V4_p2',
    'mA 5_p2',
    'V5_p2',
    'T7 - COM14_t1',
    'mA 6_p2',
    'V6_p2',
    'mA 7_p2',
    'V7_p2',
    'T8 - COM14_t1',
    'mA 8_p2',
    'V8_p2'
]

combined_data_ordered = combined_data[order].to_csv(f'combined_data.csv_{timestamp}', index=False)

#combined_data.to_csv(f'combined_data.csv_{timestamp}', index=False) #index=False removes the labing index that is to the left of the data by default e.g. 1,2,3,4,5,6,7,...,n
