# documentation for 9/29/25 *github doesnt like breaklines, so double pardon formatting*
John Sarrouf Report for Hydrogen Sensor 9/29
After much tinkering and research as to how the sensors work and how we can convert the raw DAC data that we get from the pinout to a usable PPM reading, we now have a working matching set of programs for both the pi pico and the computer. The pico side of things gathers the raw data and converts it into the ppm data that we need, it then outputs the data in a convenient csv format. On the computer side of things, it is listening for the pico and takes the printout from the pico and writes it to both the screen and an appropriately named csv file on the computer.

in terms of how the data is handled it follows the following "path"

raw dac (digital analog converter) data is read from pinout on the pico sensor
>
then the data is converted using the following formula that is used in dac to voltage / ppm
outMin + (float(voltage - inMin) / float(inMax - inMin)) * (outMax - outMin)

the inmax is the resolution of the dac, and for some circuits is two to the power of the number of resistors in the circuit
for our purposes it is sixteen

the outmax is the reference voltage, which is the output voltage from the pico which is 3.3 V

the output is a  value that represents the voltage to ppm ratio that we can use to derive the ppm later on

NEXT
we take the reciprocal of the output of the above function divided by the reference voltage divided by the max ppm that the sensor can read out
in plain english this doesnt make any sense, for how the process / math actually looks i would check the code which is linked below

and then thats basically it
ALL steps of the data processing are saved as to avoid losing ANY kind of info 

hydrogen sensor code on repo v2

version0 is deprecated, but for version control i kept it
also pardon the terrible formatting 
