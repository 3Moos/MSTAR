#import uarray as array
import array
#import csv
import random
from time import sleep

# Replace 'file.csv' with your actual CSV file path
csv_file = '1_degree.csv'
data = []

delim = ','
with open(csv_file,'r') as file:
    for line in file:
        #print(line)
        line = line.strip().replace('ufeff', '')
        data.append(line.rstrip('\n').rstrip('\r').split(delim))

pt100_table = [(float(x.strip().replace('\ufeff', '')), float(y.strip().replace('\ufeff', ''))) for x, y in data]


def get_temperature(resistance):
    """Interpolates the temperature from the lookup table."""
    for i in range(len(pt100_table) - 1):
        if pt100_table[i][0] <= resistance <= pt100_table[i + 1][0]:
            r1, t1 = pt100_table[i]
            r2, t2 = pt100_table[i + 1]
            return t1 + (resistance - r1) * (t2 - t1) / (r2 - r1)
    return None  # Return None if resistance is out of range

    
    
