#!/bin/bash

set -e

# Optional: Activate virtual environment if needed
if [ -d "venv" ]; then
    echo "[*] Activating virtual environment"
    source venv/bin/activate
fi

# Default serial port (can be overridden)
SERIAL_PORT=${1:-/dev/ttyACM0}

echo "[*] Starting AmigaRTK with serial port: $SERIAL_PORT"

# Run the program
amigartk --serial-port "$SERIAL_PORT"
#!/bin/bash

set -e
source venv/bin/activate

SERIAL_PORT=${1:-/dev/ttyACM0}
echo "Launching AmigaRTK with $SERIAL_PORT"
python -m main --serial-port "$SERIAL_PORT"
