import analogio
from board import *
from time import sleep
import wifi
import socketpool
import adafruit_requests
import os
import json
from config import config

# define the pins for the respective voltage sensors
pin = analogio.AnalogIn(A0)
pin2 = analogio.AnalogIn(A1)

# voltage is the DAC VALUE readout from the sensor
# inmax is 2^16 and is our resolution for the DAC
# outmax is the reference voltage, 3.3 V from pico
# output is the voltage / ppm value
# some of the variable might not appear to mean anything, but this is moreso a general formula for this kind of sensor
def dac_to_ppm_ratio(voltage, inMin = 0.0, inMax = 65535, outMin = 0.0, outMax = 3.3):
  return outMin + (float(voltage - inMin) / float(inMax - inMin)) * (outMax - outMin)

# set to run indefinitely, will likelly be changed in the future to account for the experiment needing to end

# index to show how many times sensor has run, important because pico and computer might not start at the same time
# ppm_mult is determined based off of the reference voltage from the pico (3.3) divided by the max value that can be read (ppm)
reading_index = 0
ppm_multiplier = 3.3/20000

while True:

    # gets the dac reading from that pin in order to calculate the ppm later on
    dac = pin.value
    dac2 = pin2.value

    # takes the dac readings and through the formnula above, generates a voltage conversion
    voltage = dac_to_ppm_ratio(dac)
    voltage2 = dac_to_ppm_ratio(dac2)

    # little bit of funky unit conversion to get the ppm
    # IDEALLY, this results in the hydrogen ppm, but further testing is required to verify this
    # it is likely that we would see something ~.05
    converted_ppm = 1.0 / (float(voltage) / float(ppm_multiplier))
    converted_ppm2 = 1.0 / (float(voltage2) / float(ppm_multiplier))
    
    # btw, the f string formatting is just so it only shows up to a certain amount of decimals, in this case two
    print(f"Index: {reading_index}, DAC reading: {voltage}, Voltage Conversion: {ppm:,.2f}, DAC2 reading: {voltage2}, Voltage2 Conversion: {ppm2:,.2f}, PPM Conversion: {converted_ppm:,.2f}, PPM2 Conversion: {converted_ppm2:,.2f}")
    # no offense to jack, but it makes sense to format the data in csv format for the csv file
    # we can adjust things to be more visually appealing on the computer side of things
    # also, the time at reading will be inserted on the computer side of things, as the pico does not have RTC
    reading_index += 1

    # three decimals to avoid accidental scientific notation
    print(f"{dac:,.3f}, {dac2:,.3f}, {voltage:,.3f}, {voltage2:,.3f}, {converted_ppm:,.3f}, {converted_ppm2:,.3f}")
  
    sleep(1)

