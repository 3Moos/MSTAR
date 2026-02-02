# file: hydroSenseComp.py
# Reads serial data from Pico and logs to a timestamped CSV (Windows-friendly)
# - Detects COM ports via pyserial's list_ports (Windows)
# - Tries common baud rates (115200 then 9600)
# - Disables the "readline waits forever" issue via timeouts
# - Writes raw Pico line + timestamp to CSV

import os
import sys
import csv
import glob
import serial
from serial.tools import list_ports
import datetime as dt
from time import sleep

# ---------------- CONFIG ----------------
# Use a raw string for Windows paths so backslashes aren't interpreted as escapes
FOLDER_LOCATION = r"C:\Users\MSTAR\Desktop\H2 sensor test 12326"

# Candidate COM ports to try if list_ports finds nothing (fallback)
CANDIDATE_PORTS = [
    "COM6"
]

# Try these baud rates (Thonny/MicroPython REPL is often 115200)
CANDIDATE_BAUDS = [115200, 9600]

TIMEOUT_S = 2
SAMPLE_DELAY_S = 1

# CSV columns:
CSV_HEADER = ["timestamp", "value1", "value2", "value3"]
# ----------------------------------------


def find_serial_ports(override_port=None):
    """Return a list of available serial ports.

    Priority order:
    1. If override_port is specified, use only that port.
    2. Try CANDIDATE_PORTS first (these are preferred).
    3. Then add any remaining detected ports from list_ports.comports().
    Results are de-duplicated while preserving order.
    """
    if override_port:
        return [override_port]
    
    # Get all detected ports
    detected = []
    try:
        detected = [p.device for p in list_ports.comports()]
    except Exception:
        detected = []
    
    # Start with CANDIDATE_PORTS (preferred), then add any others
    ports = list(CANDIDATE_PORTS)
    for p in detected:
        if p not in ports:
            ports.append(p)
    
    return ports if ports else []


def open_pico_serial(override_port=None):
    """Try ports and bauds until one opens.
    
    If override_port is specified, try only that port.
    """
    ports = find_serial_ports(override_port=override_port)
    last_err = None

    for port in ports:
        for baud in CANDIDATE_BAUDS:
            try:
                ser = serial.Serial(port, baud, timeout=TIMEOUT_S)

                # Some boards reset / change behavior on open.
                # These settings often help on macOS.
                try:
                    ser.dtr = True
                    ser.rts = False
                except Exception:
                    pass

                sleep(2.0)  # give the Pico time to settle after open/reset
                try:
                    ser.reset_input_buffer()
                except Exception:
                    pass

                print(f"Connected to: {ser.port} @ {ser.baudrate}")
                return ser
            except Exception as e:
                last_err = e

    raise RuntimeError(
        "Could not open Pico serial.\n"
        f"Tried ports: {ports}\n"
        f"Tried bauds: {CANDIDATE_BAUDS}\n"
        f"Last error: {last_err}"
    )


def begin_file():
    """Create a timestamped CSV and return (file_handle, csv_writer)."""
    os.makedirs(FOLDER_LOCATION, exist_ok=True)
    now = dt.datetime.now()
    filename = now.strftime("%m_%d_%Y %I_%M_%S %p") + ".csv"
    path = os.path.join(FOLDER_LOCATION, filename)

    f = open(path, "w", newline="", encoding="utf-8")
    w = csv.writer(f)
    w.writerow(CSV_HEADER)
    f.flush()

    print("Logging to:", path)
    return f, w


def read_one_line(ser: serial.Serial):
    """
    Read one line from serial.
    Returns decoded string (no newline) or None if timeout/no data.
    """
    raw = ser.readline()
    if not raw:
        return None
    line = raw.decode("utf-8", errors="replace").strip()
    return line if line else None


def write_row(writer, file_handle, raw_line: str):
    """Write one CSV row and flush so you don't lose data if it crashes.
    
    Splits the raw_line by whitespace and writes each value as a separate column.
    """
    ts = dt.datetime.now().isoformat(timespec="seconds")
    values = raw_line.split()
    writer.writerow([ts] + values)
    file_handle.flush()
    


def main():
    # Parse command-line arguments
    override_port = None
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        if idx + 1 < len(sys.argv):
            override_port = sys.argv[idx + 1]
    
    # Show available ports for debugging
    print("Available COM ports:")
    try:
        available = list_ports.comports()
        if available:
            for p in available:
                print(f"  {p.device} - {p.description}")
        else:
            print("  (none detected by list_ports)")
    except Exception as e:
        print(f"  (error querying ports: {e})")
    
    if override_port:
        print(f"\nUsing specified port: {override_port}")
    
    pico = open_pico_serial(override_port=override_port)
    file_handle, writer = begin_file()

    try:
        while True:
            line = read_one_line(pico)
            if line is None:
                print("[no data]\n")
            else:
                print(f"{line}\n")
                write_row(writer, file_handle, line)

            sleep(SAMPLE_DELAY_S)

    except KeyboardInterrupt:
        print("exiting program")

    finally:
        try:
            pico.close()
        except Exception:
            pass
        try:
            file_handle.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
