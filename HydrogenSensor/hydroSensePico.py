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

# define the pins for the respective voltage sensors
pin = analogio.AnalogIn(A0)
pin2 = analogio.AnalogIn(A1)

# OUTDATED / DEPRECATED
# ~ 1
# the voltage is the value that we get from the MCP3221
# it is a highly precise voltage reading
# ~ 2
# the "in" variables are the range of the DAC readouts
# [0, 65535]
# DAC -> Digital to Audio Converter (Most Assumably)
# ~ 3
# the "out" variables are from the range in the ppm values
# this range is determined when calibrating the sensor
# at the max voltage of 3.3, the ppm read is 20000
# at the lowest voltage 0.02 ~ 0, the ppm read is 0
# for our purposes, it is set at [0, 20000]
# recalibration may be necessary, as the documentation does not have a value remotely close to this
# def voltage_to_ppm(voltage, inMin = 0.0, inMax = 65535, outMin = 0.0, outMax = 20000.0):
#  return outMin + (float(voltage - inMin) / float(inMax - inMin) * (outMax - outMin))

# ADD PROPER DOCUMENTATION
# voltage is the DAC VALUE readout from the sensor
# inmax is 2^16 and is our resolution for the DAC
# outmax is the reference voltage, 3.3 V from pico
def voltage_to_ppm(voltage, inMin = 0.0, inMax = 65535, outMin = 0.0, outMax = 3.3):
  return outMin + (float(voltage - inMin) / float(inMax - inMin)) * (outMax - outMin)

# set to run indefinitely, will likelly be changed in the future to account for the experiment needing to end 
while True:

    # gets the voltage from that pin in order to calculate the ppm later on
    voltage = pin.value
    voltage2 = pin2.value

    # takes the voltages and through the formnula above, generates a ppm
    ppm = voltage_to_ppm(voltage)
    ppm2 = voltage_to_ppm(voltage2)

    # ~ 1
    # the ranges of the outputs should match those of the voltage_to_ppm function as seen above
    # for debugging purposes of course, though i am not sure of setting the ranges will cause problems later
    # ~ 2
    # btw, the f string formatting is just so it only shows up to a certain amount of decimals, in this case two
    # print(f"DAC reading: {voltage}, PPM Conversion: {ppm:,.2f}")
    # print(f"DAC2 Voltage: {voltage2}, PPM Conversion: {ppm2:,.2f}\n")

    # for csv purposes
    print(string(voltage) + "," + string(voltage2) + "," + string(ppm) + "," + string(ppm3))

    sleep(1)

