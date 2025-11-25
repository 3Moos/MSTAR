import board
import busio
import digitalio
from time import sleep
from adafruit_ina219 import INA219
import adafruit_max31865
import usb_cdc
import time
from time import monotonic
from pt100_lookuptable import get_temperature

spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12)
i2c = busio.I2C(board.GP15, board.GP14)
temp1_cs = digitalio.DigitalInOut(board.GP18)
temp2_cs = digitalio.DigitalInOut(board.GP19)
temp1_sensor = adafruit_max31865.MAX31865(spi, temp1_cs)
temp2_sensor = adafruit_max31865.MAX31865(spi, temp2_cs)

print("Scanning I2C bus...")
i2c.try_lock()
devices = i2c.scan()
i2c.unlock()

flip_time = 3

if devices:
    print("Found I2C devices:", devices)
else:
    print("No I2C devices found.")
    
power_sensor = INA219(i2c)

true_p = digitalio.DigitalInOut(board.GP17)
true_p.direction = digitalio.Direction.OUTPUT

false_p = digitalio.DigitalInOut(board.GP16)
false_p.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# LED flashing variables
flash_count = 0
led_on = False
last_flash_time = time.monotonic()
flashing = True
desired_flash_time = 0.25
number_flashes = 6; number_flashes *= 2
number_flashes = int(number_flashes)

# ----------------------------
# NEW: Reading loop control flag
# ----------------------------
reading_loop_active = False

def get_header():
    header = "resistance, temp_1, temp_2, power on/off, power W, voltage, current"
    print(header)

def flash_led():
    global flash_count, led_on, last_flash_time, flashing
    if flashing:
        current_time = time.monotonic()
        if current_time - last_flash_time >= desired_flash_time:
            led_on = flash_count % 2 == 0
            led.value = led_on
            last_flash_time = current_time
            flash_count += 1
            if flash_count >= number_flashes:
                flashing = False

def led_on():
    led.value = True
    print("LED turned ON")

def led_off():
    led.value = False
    print("LED turned OFF")

def power_on():
    true_p.value = True
    led.value = True
    print('power on')
    
def power_off():
    true_p.value = False
    led.value = False
    print('power off')

def get_temp():
    temp_1 = temp1_sensor.temperature
    temp_2 = temp2_sensor.temperature
    print(f"{temp_1}, {temp_2}")

# ----------------------------
# Original get_reading
# ----------------------------
def get_reading():
    return 1 if true_p.value else 0

# ----------------------------
# One-shot full reading
# ----------------------------
def take_reading():
    power_test = 1 if true_p.value else 0

    voltage = power_sensor.bus_voltage
    current = power_sensor.current
    power = power_sensor.power

    temp_1 = temp1_sensor.temperature
    temp_2 = temp2_sensor.temperature

    if current > 2.3:
        corrected_current = current - 2.3
        resistance = abs(voltage / (corrected_current / 1000))
    else:
        corrected_current = 0
        resistance = 0

    data = f"{resistance},{temp_1},{temp_2},{power_test},{power},{voltage},{corrected_current}"
    print(data)

# ----------------------------
# Non-blocking reading loop tick
# ----------------------------
def reading_loop_tick():
    if reading_loop_active:
        take_reading()
        sleep(1)  # spacing between readings

def clear_serial_buffer():
    while usb_cdc.console.in_waiting > 0:
        usb_cdc.console.read()

# ----------------------------
# Main USB command listener
# ----------------------------
def listen_for_commands():
    global reading_loop_active
    while True:
        # Run reading loop if active
        reading_loop_tick()

        try:
            if usb_cdc.console.in_waiting > 0:
                led.value = True
                led.value = False

                command = usb_cdc.console.readline().decode('utf-8').strip()

                if command == "led_on":
                    led_on()
                elif command == "led_off":
                    led_off()
                elif command == "power_on":
                    power_on()
                elif command == "power_off":
                    power_off()
                elif command == "get_readings":
                    take_reading()
                elif command == "flash_led":
                    flash_led()
                elif command == "get_header":
                    get_header()
                elif command == "get_temp":
                    get_temp()
                elif command == "reading_loop_start":
                    reading_loop_active = True
                    print("Reading loop started")
                elif command == "reading_loop_stop":
                    reading_loop_active = False
                    print("Reading loop stopped")
                else:
                    print("Unknown command")
        except Exception as e:
            print(f"Error: {e}")

listen_for_commands()