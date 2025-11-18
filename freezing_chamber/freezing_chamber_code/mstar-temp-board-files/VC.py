import board
import busio
import digitalio
from time import sleep
from adafruit_ina219 import INA219
import adafruit_max31865


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
    
device = INA219(i2c)

true_p = digitalio.DigitalInOut(board.GP17)
true_p.direction = digitalio.Direction.OUTPUT

false_p = digitalio.DigitalInOut(board.GP16)
false_p.direction = digitalio.Direction.OUTPUT


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

true_p.value = True


while True:
    #print(device.bus_voltage, device.current, device.power, device.bus_voltage/((device.current - 2)/1000))
    print(temp1_sensor.temperature, temp2_sensor.temperature)
    sleep(0.5)
