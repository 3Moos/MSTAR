## brief summary
the ina219 is a voltage / current sensor, it allows the use of TWO multimeters for further data collection and analysis
<br>within the scope of the research, it is for determining the current that is going through the membrane, and also possibly to "calibrate" other sensors that might need a voltage / current value to approximate their sensor readout

## other technical details
depending on WHICH version of the ina219 that we have, we are either within 1% or .5% of the actual value (some weird chip shortage thingy)
<br>in terms of the values that it can read out, it depends on the "gain" of the sensor, which can be read off like so
<br>
'''
import board
import busio
import adafruit_ina219
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ina219.INA219(i2c)

print(sensor.gain())
'''

<br>
basically, depending on the range that the sensor reads out (the current readouts)
<br>either ±3.2A or ±400mA, the resolution will be **0.8mA and .1mA respectively**
<br>
**in conclusion kaden (@3Moos), i can only assume that you are using the latter resolution**
**and therefore, the .3mA readout that you are getting IS valid, and not just zero being read out incorrectly**
<br>
*additional notes, the sensor is susceptible to damage if the polarity is changed rapidly*
*and it seems that there is literally a polarity switcher ON the board, just figured it should be noted*

<br>[ina219 datasheet](https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout?view=all)

![md visualized here](https://github.com/3Moos/MSTAR/blob/main/documentationGeneral/Screenshot_2025-10-08_06-22-23.png?raw=true)
