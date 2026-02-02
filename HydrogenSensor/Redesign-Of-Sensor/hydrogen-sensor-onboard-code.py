from machine import ADC, Pin
from time import sleep

# ADC setup (RP2040 = 16-bit scaled)
adc1 = ADC(Pin(26))  # A0
adc2 = ADC(Pin(27))  # A1
adc3 = ADC(Pin(28))  # A2

REF_VOLTAGE = 3.3
MAX_ADC_VALUE = 65535

V_MIN1 = 0.086824
V_MIN2 = 0.02
V_MIN3 = 0.067111
V_MAX = 3.0
PPM_MIN1 = 0
PPM_MIN2 = 0
PPM_MIN3 = 0
PPM_MAX = 20000

def adc_to_voltage(raw):
    return (raw / MAX_ADC_VALUE) * REF_VOLTAGE

def calculate_ppm1(voltage):
    if voltage <= V_MIN1:
        return PPM_MIN1
    elif voltage >= V_MAX:
        return PPM_MAX
    else:
        return (PPM_MAX - PPM_MIN1) * (voltage - V_MIN1) / (V_MAX - V_MIN1)

def calculate_ppm2(voltage):
    if voltage <= V_MIN2:
        return PPM_MIN2
    elif voltage >= V_MAX:
        return PPM_MAX
    else:
        return (PPM_MAX - PPM_MIN2) * (voltage - V_MIN2) / (V_MAX - V_MIN2)

def calculate_ppm3(voltage):
    if voltage <= V_MIN3:
        return PPM_MIN3
    elif voltage >= V_MAX:
        return PPM_MAX
    else:
        return (PPM_MAX - PPM_MIN3) * (voltage - V_MIN3) / (V_MAX - V_MIN3)
    

while True:
    raw1 = adc1.read_u16()
    raw2 = adc2.read_u16()
    raw3 = adc3.read_u16()

    v1 = adc_to_voltage(raw1)
    v2 = adc_to_voltage(raw2)
    v3 = adc_to_voltage(raw3)

    ppm1 = calculate_ppm1(v1)
    ppm2 = calculate_ppm2(v2)
    ppm3 = calculate_ppm3(v3)
    print(ppm1, v1, " ", ppm2, v2, " ", ppm3, v3)
    sleep(1)
