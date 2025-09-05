from serial import Serial
from time import sleep
import serial.tools.list_ports
#from ser_chamber import find_chamber, send, set_temp, turn_on, turn_off, get_temp


class chamber_controller():
    def _init_(self):
        self.chamber = find_chamber()
        self.chamber.flushInput()   
        
    def find_chamber():
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Prolific" in port.description:
                return Serial(port.device, baudrate=19200, timeout=0.25)
        return None

    def send(command, chamber = None):
        
        if chamber is None:
            chamber = find_chamber()

        if chamber:
            # chamber.flushInput()
            # chamber.flushOutput()
            # chamber.reset_input_buffer()
            # chamber.reset_output_buffer()
            response = chamber.write(command)
            response = chamber.readlines()

            print(response)
            return response
        else:
            print("Prolific port not found")
            return "False"
        
    def set_temp(float=20.0):
        command = f"= SP1 {float}\r\n"
        find_chamber(command)
        
    def turn_on():
        find_chamber("= ON\r\n")
        
    def turn_off():
        find_chamber("= OFF\r\n")
        
    def get_temp(chamber = None):
        if chamber is None:
            chamber = find_chamber()
            
        return(send(b"? SP1", chamber))

# chamber = find_chamber()
# send(b"= SP1 0\r\n", chamber)
# print(chamber.readline())
# get_temp(chamber)
# chamber.close()