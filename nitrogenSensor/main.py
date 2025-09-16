import analogio
from board import *
from time import sleep
import wifi
import socketpool
import adafruit_requests
import os
import json
from config import config

#network_data = []

# with open('network_config.json', 'w') as f:
#     print(network_data)
    #json.dump(network_data, f, indent=2)

pin = analogio.AnalogIn(A0)
pin2 = analogio.AnalogIn(A1)

def reverse_string(s):
    result = ''
    for char in s:
        result = char + result
    return result

def add_commas(number):
#     print("Number is ", number)
    num_str = str(number)

    decimals = num_str.split(".")
    
    length = len(decimals)
    
    add_commas = length % 3
    
    
    print(decimals[1], add_commas)
    split_string = decimals[1]
    current_comma = 3
    print("SPLIT IS", split_string[2])
    data = ""
    for count, char in enumerate(split_string):
        data += char
        print(data)
        
        if count == add_commas - 1:
            data += ","
            add_commas += 3
            
    return float(decimals[0])



def voltage_to_ppm(voltage, inMin = 0, inMax = 3.3, outMin = 0, outMax = 20000):
  return outMin + (float(voltage - inMin) / float(inMax - inMin) * (outMax
                  - outMin))

while True:
    voltage = pin.value
    voltage2 = pin2.value
    #ppm = add_commas(voltage_to_ppm(voltage))
    ppm = voltage_to_ppm(voltage)
    ppm2 = voltage_to_ppm(voltage2)
    print(f"DAC reading: {voltage}, PPM Conversion: {ppm:,.2f}")
    print(f"DAC2 Voltage: {voltage2}, PPM Conversion: {ppm2:,.2f}\n")
    sleep(1)

