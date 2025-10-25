# file name -> hydroSenseComp.py
# reads data from pico, saves data to csv
# most, if not all, of the code is taken from one of my older repos
# https://github.com/llaammbbddaa/jacksonSix

# pico is likely on COM 3
# in terms of "!=" vs "is not", we almost always use the comparison to the "None" data type, and as such, "is not" makes sense as it is for comparing data types

import serial
import os
from time import sleep
import datetime

# sets up serial on COM 3 (where the pico is, at least for testing) and at a BAUD rate of 9600
def beginSerial():
    ser = serial.Serial("/dev/tty.usbmodem1101", 9600, timeout = 4)
    return ser


# creates file and whatnot
def beginFile():
    
    # current data
    now = datetime.datetime.now()
    
    
    #data is formatted for file name
    folder_location = "/Users/moose/Documents/MSTAR_Code/MSTAR/hydrogensensor"
    os.makedirs(folder_location, exist_ok=True) ##
    formatted_date_time = now.strftime("%m_%d_%Y %I_%M_%S %p")
    formatted_date_time = os.path.join(folder_location, formatted_date_time + ".csv")
    print(formatted_date_time)
    #adding file for branch merging
    # checks if file exists, and if not creates one
    if (os.path.exists(formatted_date_time)):
        file = open(formatted_date_time, "a")
        file.write("\n")
    else:
        file = open(formatted_date_time, "w")
        # if file is brand new, add the formatting stuff
        file.write("timestamp, volt1 V, volt2 V, H ppm1, H ppm2\n")
    
    # returns file such that it can be used all around
    return file

# begin writing to text file
def beginWrite(pico = None, file = None):
    current_time_stamp = datetime.datetime.now()
    # if either pico or file arent present, the code doesnt run to ensure that no errors o>
    if pico is not None and file is not None:

        # added current time stamp, and only referencing pico once rather than twice to reduce error
        line = pico.readline().decode("utf-8").strip()
        if not line:
            print("[no data]")
            return
        print(line)  # same format as Pico output
        csv_line = f"{current_time_stamp.isoformat(timespec='seconds')},{line}"
        file.write(csv_line + "\n")
        file.flush()

        # to reduce risk of program crashing and losing data
        # force writes data to drive without closing the file entirely
        file.flush()
    else:
        if pico is None:
            print("pico is none")
        else:
            print("file is none")

# the real stuff begins here
# various init
pico = beginSerial()
file = beginFile()

print("Connected to:", pico.name)


if __name__ == "__main__":
    try:
        while True:
            # reads data from pico, (print output)
            # writes read data to csv file
            # waits for a second before reading more (data gathering program is also set to wait one second)
            beginWrite(pico, file)
            sleep(1)

    except KeyboardInterrupt:
        print("exiting program")
        pico.close()
        file.close()
        exit(0)
