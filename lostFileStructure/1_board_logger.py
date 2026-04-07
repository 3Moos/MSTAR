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

pico1 = Serial('COM14', 115200, timeout=2)
picos = [pico1]

testing_temperature = str(testing_temperature) + "C"

board_1 = "board1 - COM27"

temp_boards = file_name + " " + testing_temperature + "Temp Boards - COM15" ##-COM18-COM16-COM14
board_1 = board_1 + " " + testing_temperature

# Create a new folder for storing the logs
folder_name = "logs " + timestamp

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Add the folder location to the file_name

file_name = os.path.join(folder_name, temp_boards)
file_name = f"{file_name} {timestamp}.csv"

board1_name = os.path.join(folder_name, board_1 + " " + timestamp + ".csv")

name1 = os.path.join(folder_name, " temps " + timestamp + ".csv")


print(name1, "\n")
print(file_name)

        
with open(name1, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header to the CSV file
    csvwriter.writerow(['Timestamp', 'T1 - COM15', 'T2 - COM15', 'T3 - COM18', 'T4 - COM18', 'T5 - COM16', 'T6 - COM16', 'T7 - COM14', 'T8 - COM14'])


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
                
        
        with open(name1, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')
            # Write the timestamp and the line to the CSV file
            data = data.split(", ")
            data.insert(0, timestamp)
            csvwriter.writerow(data)
        

    
        print("Temp 1-8 : " + print_data)
        sleep(0.5) # Adjust the sleep time as needed
            
            
    except KeyboardInterrupt:
        print("Exiting...")
        for pi in picos:
            pi.close()
        break
    
    
    
