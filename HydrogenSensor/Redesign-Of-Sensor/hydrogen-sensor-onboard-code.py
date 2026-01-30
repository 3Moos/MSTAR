from machine import ADC, Pin
from time import sleep

# ADC setup (RP2040 = 16-bit scaled)
adc1 = ADC(Pin(26))  # A0
adc2 = ADC(Pin(27))  # A1
adc3 = ADC(Pin(28))  # A2

REF_VOLTAGE = 3.3
MAX_ADC_VALUE = 65535

V_MIN = 0.02
V_MAX = 3.0
PPM_MIN = 0
PPM_MAX = 20000

def adc_to_voltage(raw):
    return (raw / MAX_ADC_VALUE) * REF_VOLTAGE

def calculate_ppm(voltage):
    if voltage <= V_MIN:
        return PPM_MIN
    elif voltage >= V_MAX:
        return PPM_MAX
    else:
        return (PPM_MAX - PPM_MIN) * (voltage - V_MIN) / (V_MAX - V_MIN)

while True:
    raw1 = adc1.read_u16()
    raw2 = adc2.read_u16()
    raw3 = adc3.read_u16()

    v1 = adc_to_voltage(raw1)
    v2 = adc_to_voltage(raw2)
    v3 = adc_to_voltage(raw3)

    ppm1 = calculate_ppm(v1)
    ppm2 = calculate_ppm(v2)
    ppm3 = calculate_ppm(v3)

    print(ppm1, ppm2, ppm3)
    print(v1, v2, v3)
    print("          ")
    sleep(1)
    print(ppm1, ppm2, ppm3)
    sleep(1)
