# TODO - add csv writing

import analogio
from board import *
from time import sleep
import wifi
import socketpool
import adafruit_requests
import os
import json
from config import config

# define the pins for the respective nitrogen sensors (for reading voltage)
pin = analogio.AnalogIn(A0)
pin2 = analogio.AnalogIn(A1)

# NEED TO FIND WHAT EACH VAR REPRESENTS
# will be determined once part name is found
def voltage_to_ppm(voltage, inMin = 0, inMax = 3.3, outMin = 0, outMax = 20000):
  return outMin + (float(voltage - inMin) / float(inMax - inMin) * (outMax - outMin))

# set to run indefinitely, will likelly be changed in the future to account for the experiment needing to end 
while True:

    # gets the voltage from that pin in order to calculate the nitrogen ppm later on
    voltage = pin.value
    voltage2 = pin2.value

    # takes the voltages and through the formnula above, generates a ppm
    ppm = voltage_to_ppm(voltage)
    ppm2 = voltage_to_ppm(voltage2)

    # btw, the f string formatting is just so it only shows up to a certain amount of decimals, in this case two
    print(f"DAC reading: {voltage}, PPM Conversion: {ppm:,.2f}")
    print(f"DAC2 Voltage: {voltage2}, PPM Conversion: {ppm2:,.2f}\n")

    sleep(1)

