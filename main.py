import asyncio
import serial
from pyubx2 import UBXReader
from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.pose_pb2 import Pose
from google.protobuf.timestamp_pb2 import Timestamp
from pathlib import Path
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 115200

# Set your GPS-to-local-frame converter here if needed.
def latlon_to_pose(lat, lon, alt):
    # Example: simplistic ENU offset (replace with UTM or GPS->Map projection if needed)
    pose = Pose()
    pose.position.x = lat  # Use transformed X
    pose.position.y = lon  # Use transformed Y
    pose.position.z = alt  # Altitude
    pose.rotation.w = 1.0  # Identity quaternion
    return pose

async def main():
    # Load the event service config
    service_config = EventServiceConfig()
    service_config.name = "amiga_rtk"
    service_config.uri.host = "localhost"
    service_config.uri.port = 50051
    client = EventClient(service_config)

    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1) as stream:
        ubr = UBXReader(stream)

        print(f"Connected to GPS on {SERIAL_PORT} at {BAUDRATE} baud.")

        while True:
            try:
                (_, msg) = ubr.read()
                if msg.identity == 'NAV-PVT' and msg.fixType >= 4:  # RTK Fixed/Float
                    lat = msg.lat / 1e7
                    lon = msg.lon / 1e7
                    alt = msg.hMSL / 1000.0  # mm to meters

                    pose = latlon_to_pose(lat, lon, alt)
                    timestamp = Timestamp()
                    timestamp.GetCurrentTime()
                    pose.acquisition_time.CopyFrom(timestamp)

                    print(f"RTK Pose: lat={lat}, lon={lon}, alt={alt}")
                    await client.request_reply("/filter/pose", pose)
            except Exception as e:
                print(f"GPS read error: {e}")
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down.")
