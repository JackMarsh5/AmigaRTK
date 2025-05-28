import asyncio
import serial
from pyubx2 import UBXReader
from datetime import datetime

SERIAL_PORT = '/dev/ttyACM0'  # Change if different
BAUDRATE = 115200

async def read_gps_data():
    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as stream:
        ubr = UBXReader(stream)

        print(f"[{datetime.now()}] Connected to GPS on {SERIAL_PORT} at {BAUDRATE} baud.")
        while True:
            try:
                (_, parsed_data) = ubr.read()
                if parsed_data.identity == 'NAV-PVT':
                    print(f"Time: {parsed_data.hour}:{parsed_data.min}:{parsed_data.sec}, "
                          f"Lat: {parsed_data.lat/1e7}, Lon: {parsed_data.lon/1e7}, "
                          f"Alt: {parsed_data.hMSL/1000} m, Fix: {parsed_data.fixType}, "
                          f"Num SVs: {parsed_data.numSV}")
            except Exception as e:
                print(f"Error reading GPS data: {e}")
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    try:
        asyncio.run(read_gps_data())
    except KeyboardInterrupt:
        print("\nTerminated by user.")

