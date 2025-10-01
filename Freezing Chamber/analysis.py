import csv
import pandas
import pandas as pd #Allows for data manipulation 
import numpy as np 
import time
from pathlib import Path 
import os 

df_p1 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ power 1 09-27-2025-Sat 11-54-29-AM.csv') 
df_p2 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ power 2 09-27-2025-Sat 11-54-29-AM.csv') 
df_t1 = pd.read_csv('/Users/moose/Documents/MSTAR - Code/MSTAR/Freezing Chamber/ temps 09-27-2025-Sat 11-54-29-AM.csv') 

df_p1 = df_p1.apply(pd.to_numeric, errors="coerce") 
df_p2 = df_p2.apply(pd.to_numeric, errors="coerce") 
df_t1 = df_t1.apply(pd.to_numeric, errors="coerce") 

#=combined_data = df[(df['mA 1'] <= .1) & (df['V1'] > 5)] #Filters the data to only take values when mA 1 is less than .1 and V1 is more than 5 
 
power_data_p1 = df_p1[(df_p1['V1'] > 5)] 
power_data_p2 = df_p2[(df_p2['V1'] > 5)]  
temp_data_t1 = df_t1[(df_t1['T1 - COM15'] < 33)] 

combined_data = pd.concat([power_data_p1, power_data_p2, temp_data_t1], axis=1) 

combined_data.to_csv('combimed_data.csv') 