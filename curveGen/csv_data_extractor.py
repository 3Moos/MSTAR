import csv
import pandas
import pandas as pd #Allows for data manipulation
import numpy as np
import time
from pathlib import Path

current_time = time.localtime()
current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)


file = "/Users/moose/Library/Mobile Documents/com~apple~CloudDocs/MSTAR/MSTAR/curveGen/07082025 10% CaClO4 30% sat ink 18V NEW fine JSC W temp SENSOR 2 cell 7.5 NN.csv"

with open(file, 'r', newline ="") as csvfile:
    reader = csv.reader(csvfile) #treats each line as a string

    #for row in reader:
        #print(row) # Each 'row' is a list of strings representing the columns


df = pd.read_csv(file) 

rf = df[df["Latest: Current (A)"] > 0] #Gives all times
first_row = rf.iloc[0] #inside df gives boolean values to rows that meet condition, outside df hides rows that are false.
last_row = rf.iloc[-1]
temp = rf["Latest: Temperature (°C)"]
current = rf["Latest: Current (A)"]
oxygen = rf["Latest: Oxygen Gas (ppm)"]
times = rf["Latest: Time (s)"]
times_start = int(first_row["Latest: Time (s)"])
times_end = int(last_row["Latest: Time (s)"])
temp_start = int(first_row["Latest: Temperature (°C)"])
temp_end = int(first_row["Latest: Temperature (°C)"])
current_start = int(first_row["Latest: Current (A)"])
current_end = int(first_row["Latest: Current (A)"])
av_temp = temp.mean()
stdev_temp = temp.std()
temp_delta = int(current_end - current_start)
av_current = current.mean()
stdev_current = current.std()
current_delta = int(temp_end - temp_start)
oxygen_production = np.trapezoid(oxygen, times)

run_time = int(times_end - times_start) #seconds

#print(f"{av_temp}")
#print(f"{stdev_temp}")
#print(f"{integral}")

#data = (f"{file}, 'conc', 'sat', {times_start}, {run_time}, {av_current}, {stdev_current}, 'dc', {av_temp}, {stdev_temp}, 'dt', {oxygen_production}")
concentration = "conc"
saturation = "sat"
row = [
    Path(file).name, 
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


analysis = (f"analysis_csv_only - {current_date_time}.csv")

with open(analysis, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    #wrties the header to the csv file
    csvwriter.writerow(["File Name", "Concentration", "Saturation", "Start time", "Run time", "Mean Current", "Current stdev", "Delta Current", "Mean Temp", "Temp STDEV", "Delta Temp", "Oxygen Production"])
    csvwriter.writerow(row)

print("analysis complete.")