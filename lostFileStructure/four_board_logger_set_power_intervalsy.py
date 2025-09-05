'''
Adjust the following variables to reflect the current test 
The date and time stamp will be added automatically.
'''
file_name = "temp-resistance_log"
testing_temperature = -50
############################################################

from serial import Serial
from time import sleep
import csv
from datetime import datetime
import os
import threading

timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')

pico1 = Serial('COM15', 115200, timeout=2)
pico2 = Serial('COM18', 115200, timeout=2)
pico3 = Serial('COM16', 115200, timeout=2)
pico4 = Serial('COM14', 115200, timeout=2)
picos = [pico1, pico2, pico3, pico4]

power1 = Serial('COM20', 115200, timeout=2)
power2 = Serial('COM23', 115200, timeout=2)
#power3 = Serial('COM22', 115200, timeout=2)
#power4 = Serial('COM21', 115200, timeout=2)
powers = [power1, power2] #, power3, power4]

testing_temperature = str(testing_temperature) + "C"

board_1 = "board1 - COM20"
board_2 = "board2 - COM23"

temp_boards = file_name + " " + testing_temperature + "Temp Boards - COM15-COM18-COM16-COM14"
board_1 = board_1 + " " + testing_temperature
board_2 = board_2 + " " + testing_temperature

# Create a new folder for storing the logs
folder_name = "logs " + timestamp

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Add the folder location to the file_name
file_name = os.path.join(folder_name, temp_boards)
file_name = f"{file_name} {timestamp}.csv"

board1_name = os.path.join(folder_name, board_1 + " " + timestamp + ".csv")
board2_name = os.path.join(folder_name, board_2 + " " + timestamp + ".csv")

name1 = os.path.join(folder_name, " temps " + timestamp + ".csv")
name2 = os.path.join(folder_name, " power 1 " + timestamp + ".csv")
name3 = os.path.join(folder_name, " power 2 " + timestamp + ".csv")

print(name1, "\n", name2, "\n", name3, "\n")

print(file_name)


def toggle_power():
    run_power = 0
    power_on = False

    while True:
        input("Press Enter to toggle power (on/off): ")
        power_on = not power_on
        command = b'power_on\r\n' if power_on else b'power_off\r\n'
        for power in powers:
            power.write(command)

        if power_on:
            run_power += 1
        else:
            run_power = 0
        
        if run_power >= 15 and power_on:
            run_power = 0  # Reset the power cycle counter
            power1.write(b'power_off\r\n')
            power2.write(b'power_off\r\n')
            power_on = False  # Turn power off
            print("POWER OFF(Auto Shutoff)")

        print("Power turned", "ON" if power_on else "OFF")
        sleep(0.5)






# Start the toggle_power function in a separate thread
threading.Thread(target=toggle_power, daemon=True).start()

        #print("Temp 1-8 : " + print_data)
        
with open(name1, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header to the CSV file
    csvwriter.writerow(['Timestamp', 'T1 - COM15', 'T2 - COM15', 'T3 - COM18', 'T4 - COM18', 'T5 - COM16', 'T6 - COM16', 'T7 - COM14', 'T8 - COM14'])

with open(name2, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header to the CSV file
    csvwriter.writerow(['Timestamp', "mA 1", "V1", "mA 2", "V2", "mA 3", "V3", "mA 4", "V4", "mA 5", "V5", "mA 6", "V6", "mA 7", "V7", "mA 8", "V8"])

with open(name3, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header to the CSV file
    csvwriter.writerow(['Timestamp', "mA 1", "V1", "mA 2", "V2", "mA 3", "V3", "mA 4", "V4", "mA 5", "V5", "mA 6", "V6", "mA 7", "V7", "mA 8", "V8"])

while True:
    try:
        counter = 1
        data = ""
        print_data = ""
        for pi in picos:
            pi.write(b'get_temp\r\n')
            line = pi.readline()
            line = line.decode().strip()
            print_line = line        
            print_line = print_line.replace(",", "")
            
            if counter != 4:
                line += ", "
                print_line += " #|# "
            
            #print(line)
            print_data += print_line
            data += line
            counter += 1
                
        power1.reset_input_buffer()
        power1.write(b'get_readings\r\n')
        power_line1 = power1.readline()
        power_line1 = power_line1.decode().strip()

        
        power2.reset_input_buffer()
        power2.write(b'get_readings\r\n')
        power_line2 = power2.readline()
        power_line2 = power_line2.decode().strip()
        
        with open(name1, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')
            # Write the timestamp and the line to the CSV file
            data = data.split(", ")
            data.insert(0, timestamp)
            csvwriter.writerow(data)
        
        #if power_line1 != "" and power_line2 != "":
            
        with open(name2, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write the timestamp and the line to the CSV file
            #timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            data = power_line2.split(",")
            data.insert(0, timestamp)
            csvwriter.writerow(data)
        
        with open(name3, '+a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write the timestamp and the line to the CSV file
            data = power_line2.split(",")
            data.insert(0, timestamp)
            csvwriter.writerow(data)
    
        print("Temp 1-8 : " + print_data)
        print("Board 1: " + power_line1)
        print("Board 2: " + power_line2, "\n")
        #sleep(0.5) # Adjust the sleep time as needed
            
            
    except KeyboardInterrupt:
        print("Exiting...")
        for pi in picos:
            pi.close()
        break
    
    
    