import board
import busio
import digitalio
from time import sleep
from adafruit_ina219 import INA219
import adafruit_max31865
import usb_cdc


#current device name /dev/cu.usbmodem2101

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

# Define your functions that will be called based on the commands
def led_on():
    led.value = True
    print("LED turned ON")  # Print feedback for the PC to read

def led_off():
    led.value = False
    print("LED turned OFF")  # Print feedback for the PC to read

def power_on():
    print('power on')

def power_off():
    print('power off')

def get_reading():
    voltage = power_sensor.bus_voltage
    current = power_sensor.current
    power = power_sensor.power
    temp_1 = temp1_sensor.temperature
    temp_2 = temp2_sensor.temperature
    
    if current > 2:
        current = current - 2
        resistance = voltage / (current / 1000)
        resistance = abs(resistance)
        
    else:
        current = 0
        resistance = 0
    data = str(voltage) + "," + str(current) + "," + str(resistance) + ","
    data = data + str(temp_1) + "," + str(temp_2)
    print(data)
        
def clear_serial_buffer():
    while usb_cdc.console.in_waiting > 0:
        usb_cdc.console.read()  # Read and discard any data in the buffer
    
def listen_for_commands():
    clear_serial_buffer()  # Clear the buffer at the start
    while True:
        try:
            # Use usb_cdc.console instead of usb_cdc.data
            if usb_cdc.console.in_waiting > 0:
                # Read the incoming command
                command = usb_cdc.console.readline().decode('utf-8').strip()
                if command == "led_on":
                    led_on()
                elif command == "led_off":
                    led_off()
                elif command == "power_on":
                    power_on()
                elif command == "power_off":
                    power_off()
                elif command == "get_reading":
                    get_reading()
                else:
                    print("Unknown command")
        except Exception as e:
            print(f"Error: {e}")

# Start listening for commands
listen_for_commands()




