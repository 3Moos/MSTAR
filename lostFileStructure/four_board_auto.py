'''
Adjust the following variables to reflect the current test 
The date and time stamp will be added automatically.
'''
file_name = "temp-resistance_log"
testing_temperature = -20
start_temperature = 0
end_temperature = -70
current_temperature = start_temperature
temp_interval = 5
############################################################

from serial import Serial
from time import sleep
import csv
from datetime import datetime
from ser_chamber import chamber_controller
import os
import time

# try:
#     chamber = chamber_controller()
#     current_temperature = chamber.get_temp()
# except Exception as e:
#     print(f"Error initializing chamber controller: {e}")
#     chamber = None

timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')

pico1 = Serial('COM15', 115200, timeout=2)
pico2 = Serial('COM18', 115200, timeout=2)
pico3 = Serial('COM16', 115200, timeout=2)
pico4 = Serial('COM14', 115200, timeout=2)
picos = [pico1, pico2, pico3, pico4]

power1 = Serial('COM27', 115200, timeout=2)
power2 = Serial('COM28', 115200, timeout=2)
powers = [power1, power2]

testing_temperature = str(testing_temperature) + "C"

board_1 = "board1 - COM27"
board_2 = "board2 - COM28"

temp_boards = file_name + " " + testing_temperature + "Temp Boards - COM15-COM18-COM16-COM14"
board_1 = board_1 + " " + testing_temperature
board_2 = board_2 + " " + testing_temperature

# Create a new folder for storing the logs
folder_name = "logs" + timestamp
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Add the folder location to the file_name
file_name = os.path.join(folder_name, file_name)
file_name = f"{file_name} {timestamp}.csv"

print(file_name)

last_power_print = time.time()

run_power = 0
power_on = False

# Start the main loop
while True:
    try:
        # Power off after 15 cycles (or any desired threshold)
        if run_power >= 15 and power_on:
            run_power = 0  # Reset the power cycle counter
            power1.write(b'power_off\r\n')
            power2.write(b'power_off\r\n')
            power_on = False  # Turn power off
            print("POWER OFF")

        # Power on after 15 seconds of inactivity or the first time power is off
        if time.time() - last_power_print >= 600 and not power_on:
            print("RUNNING POWER")
            power1.write(b'power_on\r\n')
            power2.write(b'power_on\r\n')
            power_on = True  # Turn power on
            last_power_print = time.time()  # Reset the timer for the next power cycle

        # Increment the power cycle count only if the power is on
        if power_on:
            run_power += 1

        # Read data from each pico device
        counter = 1
        data = ""
        print_data = ""
        for pi in picos:
            pi.write(b'get_temp\r\n')
            line = pi.readline().decode().strip()
            print_line = line.replace(",", "")

            if counter != 4:
                line += ", "
                print_line += " #|# "

            print_data += print_line
            data += line
            counter += 1

        # Ensure the CSV file exists and write header if it does not
        file_exists = os.path.exists(file_name)
        with open(file_name, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            if not file_exists:
                csvwriter.writerow(['Timestamp', 'T1 - COM15', 'T2 - COM15', 'T3 - COM18', 'T4 - COM18',
                                    'T5 - COM16', 'T6 - COM16', 'T7 - COM14', 'T8 - COM14'])

            # Parse the data string and write it to the file
            temp_data = data.split(",")
            temp_data = [x.strip() for x in temp_data]  # remove whitespace
            temp_data.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # Add timestamp
            csvwriter.writerow(temp_data)

        # Read power data
        power1.reset_input_buffer()
        power1.write(b'get_readings\r\n')
        power_line1 = power1.readline().decode().strip()

        power2.reset_input_buffer()
        power2.write(b'get_readings\r\n')
        power_line2 = power2.readline().decode().strip()

        # Save power data to files
        board1_file = os.path.join(folder_name, "board1 " + os.path.basename(file_name))
        board2_file = os.path.join(folder_name, "board2 " + os.path.basename(file_name))

        with open(board1_file, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            data = power_line1.split(",")
            data.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            csvwriter.writerow(data)

        with open(board2_file, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            data = power_line2.split(",")
            data.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            csvwriter.writerow(data)

        print(f"Temp 1-8: {print_data}")
        print(f"Power Readings 1: {power_line1}")
        print(f"Power Readings 2: {power_line2}\n")

        # Optionally adjust the sleep time
        # sleep(0.5)

    except KeyboardInterrupt:
        print("Exiting...")
        for pi in picos:
            pi.close()
        break
