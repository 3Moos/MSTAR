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

timestamp = datetime.now().strftime('%m-%d-%Y-%a %H-%M-%S-%p')

pico1 = Serial('COM15', 115200, timeout=2)
pico2 = Serial('COM18', 115200, timeout=2)
pico3 = Serial('COM16', 115200, timeout=2)
pico4 = Serial('COM14', 115200, timeout=2)
picos = [pico1, pico2, pico3, pico4]

power1 = Serial('COM20', 115200, timeout=2)
power2 = Serial('COM23', 115200, timeout=2)
powers = [power1, power2]

testing_temperature = str(testing_temperature) + "C"

board_1 = "board1 - COM20"
board_2 = "board2 - COM23"

temp_boards = file_name + " " + testing_temperature + "Temp Boards - COM15-COM18-COM16-COM14"
board_1 = board_1 + " " + testing_temperature
board_2 = board_2 + " " + testing_temperature

# Create a new folder for storing the logs
folder_name = "logs" + timestamp
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Add the folder location to the file_name
file_name_all_data = os.path.join(folder_name, file_name + " All Data " + timestamp + ".csv")
file_name_power_only = os.path.join(folder_name, file_name + " Power Only " + timestamp + ".csv")

print(file_name_all_data)
print(file_name_power_only)

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

        # Collect temperature data
        counter = 1
        data = []
        print_data = ""
        for pi in picos:
            pi.write(b'get_temp\r\n')
            line = pi.readline().decode().strip()
            print_line = line.replace(",", "")
            
            if counter != 4:
                line += ", "
                print_line += " #|# "
            
            print_data += print_line
            data.append(line)  # Append temperature data as a list item
            counter += 1

        # Ensure the "All Data" log exists and write header if it does not
        if not os.path.exists(file_name_all_data):
            with open(file_name_all_data, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Timestamp', 'T1 - COM15', 'T2 - COM15', 'T3 - COM18', 'T4 - COM18', 
                                    'T5 - COM16', 'T6 - COM16', 'T7 - COM14', 'T8 - COM14'])

        # Always log temperature data to the "All Data" log
        with open(file_name_all_data, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
            data.insert(0, timestamp)  # Add timestamp at the beginning
            csvwriter.writerow(data)

        # Read power data
        power1.reset_input_buffer()
        power1.write(b'get_readings\r\n')
        power_line1 = power1.readline().decode().strip()

        power2.reset_input_buffer()
        power2.write(b'get_readings\r\n')
        power_line2 = power2.readline().decode().strip()

        # Always log power data to the "All Data" log
        with open(file_name_all_data, 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
            power_data = [timestamp, power_line1, power_line2]
            csvwriter.writerow(power_data)

        # Log data only if the power state is True
        if power_on:
            board1_file = os.path.join(folder_name, "board1 " + os.path.basename(file_name_power_only))
            board2_file = os.path.join(folder_name, "board2 " + os.path.basename(file_name_power_only))

            with open(board1_file, 'a+', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                data = power_line1.split(",")  # Split power readings by commas
                data.insert(0, timestamp)
                csvwriter.writerow(data)

            with open(board2_file, 'a+', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                data = power_line2.split(",")  # Split power readings by commas
                data.insert(0, timestamp)
                csvwriter.writerow(data)

            # Also log temperature data to "Power Only" log
            with open(file_name_power_only, 'a+', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
                # Append temperature data directly as a list, no need to split
                data_to_log = [timestamp] + data  # This can be modified as needed
                csvwriter.writerow(data_to_log)

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
