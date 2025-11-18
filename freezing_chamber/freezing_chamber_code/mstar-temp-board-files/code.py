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

#current device name /dev/cu.usbmodem2101
#from serial import Serial; pico = Serial("/dev/cu.usbmodem1101", timeout = 2);
#pico.write(b"flash_led\r\n"); pico.readline()

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
#flip_time = flip_time * 60

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

# Variables for LED flashing
flash_count = 0
led_on = False
last_flash_time = time.monotonic()
flashing = True
desired_flash_time = 0.25
number_flashes = 6; number_flashes *= 2
number_flashes = int(number_flashes)

def get_header():
    header = "resistance, temp_1, temp_2, power on/off, power W, voltage, current"
    print(header)

def flash_led():
    global flash_count, led_on, last_flash_time, flashing
    if flashing:
        current_time = time.monotonic()
        if current_time - last_flash_time >= desired_flash_time:  # Check if 0.5 seconds have passed
            led_on = flash_count % 2 == 0
            led.value = led_on  # Toggle the LED
            last_flash_time = current_time
            flash_count += 1
            if flash_count >= number_flashes:  # 3 on-off cycles
                flashing = False  # Stop flashing after 3 times
    

# Define your functions that will be called based on the commands
def led_on():
    led.value = True
    print("LED turned ON")  # Print feedback for the PC to read

def led_off():
    led.value = False
    print("LED turned OFF")  # Print feedback for the PC to read

def power_on():
    true_p.value = True
    led.value = True
    print('power on')
    
def power_off():
    true_p.value = False
    led.value = False
    print('power off')

def get_temp():
    temp_1 = temp1_sensor.temperature # - 1.64
    temp_2 = temp2_sensor.temperature # - [CYW43] Failed to start CYW43    
    print(f"{temp_1}, {temp_2}")

def get_reading():
    if true_p.value == True:
        power_test = 1
    if true_p.value == False:
        power_test = 0
    
    voltage = power_sensor.bus_voltage
    current = power_sensor.current
    power = power_sensor.power
    temp_1 = temp1_sensor.temperature # - 1.64
    temp_2 = temp2_sensor.temperature # - 1
    
    #start_time = monotonic()
    #temp_1 = get_temperature(temp1_sensor.resistance) - 0.5
    #end_time = monotonic()
    #print(end_time - start_time)
    
    #temp_2 = get_temperature(temp2_sensor.resistance) - 0.5
    
    if current > 2.3:
        current = current - 2.3
        resistance = voltage / (current / 1000)
        resistance = abs(resistance)
        
    else:
        current = 0
        resistance = 0
    data = str(voltage) + "," + str(current) + "," + str(resistance) + ","
    data = data + str(temp_1) + "," + str(temp_2) + "," + str(power_test)
    
    restructured_data = str(resistance) + "," + str(temp_1) + "," + str(temp_2) + ","
    restructured_data += str(power_test) + "," + str(power) + ","
    restructured_data += str(voltage) + "," + str(current)
    
    
    print(restructured_data)
    
    led.value = True
    sleep(0.1)
    led.value = False
    sleep(0.1)
    
def clear_serial_buffer():
    while usb_cdc.console.in_waiting > 0:
        usb_cdc.console.read()  # Read and discard any data in the buffer
    
def listen_for_commands():
    #clear_serial_buffer()  # Clear the buffer at the start

    while True:
        #flash_led()
        try:
            # Use usb_cdc.console instead of usb_cdc.data
            if usb_cdc.console.in_waiting > 0:
                led.value = True
                led.value = False
                # Read the incoming command
                command = usb_cdc.console.readline().decode('utf-8').strip()
                #print(command)
                if command == "led_on":
                    led_on()
                elif command == "led_off":
                    led_off()
                elif command == "power_on":
                    power_on()
                elif command == "power_off":
                    power_off()
                elif command == "get_readings":
                    get_reading()
                elif command == "flash_led":
                    flash_led()
                elif command == "get_header":
                    get_header()
                elif command == "get_temp":
                    get_temp()
                    
                else:
                    print("Unknown command")
        except Exception as e:
            print(f"Error: {e}")

listen_for_commands()






