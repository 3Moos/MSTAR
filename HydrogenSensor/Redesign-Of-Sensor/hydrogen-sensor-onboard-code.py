import analogio
from board import *
from time import sleep
import wifi
import socketpool
import adafruit_requests
import os
import json
from config import config

ppm_max = 20000  #This is the Linear range of the sensor
ref_voltage = 3.3  #Reference voltage of the Pico
MAX_ADC_VALUE = 65535  #16 bit ADC

V_MIN = 0.02  # Voltage at 0 ppm
V_MAX = 3.0   # Voltage at 20000 ppm
PPM_MIN = 0
PPM_MAX = 20000

pin1 = analogio.AnalogIn(A0)   
pin2 = analogio.AnalogIn(A1)
pin3 = analogio.AnalogIn(A2)

#0.02V = 0ppm
#3.0V = 20000ppm

while True:
    raw_voltage1 = pin1.value
    raw_voltage2 = pin2.value
    raw_voltage3 = pin3.value
    voltage1 = (raw_voltage1 / MAX_ADC_VALUE) * ref_voltage
    voltage2 = (raw_voltage2 / MAX_ADC_VALUE) * ref_voltage
    voltage3 = (raw_voltage3 / MAX_ADC_VALUE) * ref_voltage
    
    # Calculate PPM for each sensor
    def calculate_ppm(voltage):
        if voltage <= V_MIN:
            return PPM_MIN
        elif voltage >= V_MAX:
            return PPM_MAX
        else:
            return PPM_MIN + (PPM_MAX - PPM_MIN) * (voltage - V_MIN) / (V_MAX - V_MIN)
    
    ppm1 = calculate_ppm(voltage1)
    ppm2 = calculate_ppm(voltage2)
    ppm3 = calculate_ppm(voltage3)
