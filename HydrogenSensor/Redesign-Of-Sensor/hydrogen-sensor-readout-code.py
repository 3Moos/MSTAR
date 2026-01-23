# file: hydroSenseComp.py
# Reads serial data from Pico and logs to a timestamped CSV (macOS-friendly)
# - Uses /dev/cu.* (recommended on macOS)
# - Tries common baud rates (115200 then 9600)
# - Disables the "readline waits forever" issue via timeouts
# - Writes raw Pico line + timestamp to CSV

import os
import csv
import glob
import serial
import datetime as dt
from time import sleep

# ---------------- CONFIG ----------------
FOLDER_LOCATION = "/Users/moose/Documents/MSTAR_Code/MSTAR/hydrogensensor"

# Prefer /dev/cu.* on macOS
CANDIDATE_PORTS = [
    "/dev/cu.usbmodem*",
    "/dev/cu.usbserial*",
    "/dev/tty.usbmodem*",
    "/dev/tty.usbserial*",
    "COM3",
    "COM4",
]

# Try these baud rates (Thonny/MicroPython REPL is often 115200)
CANDIDATE_BAUDS = [115200, 9600]

TIMEOUT_S = 2
SAMPLE_DELAY_S = 1

# CSV columns:
# raw = whatever the Pico printed for that line (you can parse later)
CSV_HEADER = ["timestamp", "raw"]
# ----------------------------------------


def find_serial_ports():
    """Return a list of existing ports from glob patterns, de-duped."""
    ports = []
    for pat in CANDIDATE_PORTS:
        if "*" in pat:
            ports.extend(sorted(glob.glob(pat)))
        else:
            ports.append(pat)

    # de-dup while preserving order
    seen = set()
    out = []
    for p in ports:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def open_pico_serial():
    """Try ports and bauds until one opens."""
    ports = find_serial_ports()
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


def write_row(writer: csv.writer, file_handle, raw_line: str):
    """Write one CSV row and flush so you don't lose data if it crashes."""
    ts = dt.datetime.now().isoformat(timespec="seconds")
    writer.writerow([ts, raw_line])
    file_handle.flush()


def main():
    pico = open_pico_serial()
    file_handle, writer = begin_file()

    try:
        while True:
            line = read_one_line(pico)
            if line is None:
                print("[no data]")
            else:
                print(line)
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
