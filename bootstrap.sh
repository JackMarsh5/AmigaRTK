#!/bin/bash

set -e

# Variables
VENV_DIR="venv"

echo "[*] Creating virtual environment in ./${VENV_DIR}"
python3 -m venv $VENV_DIR

echo "[*] Activating virtual environment"
source $VENV_DIR/bin/activate

echo "[*] Upgrading pip and setuptools"
pip install --upgrade pip setuptools

echo "[*] Installing AmigaRTK package"
pip install .

echo "[*] Installation complete. Run 'source $VENV_DIR/bin/activate' to activate your environment."
echo "    Then you can run the app with 'amigartk'"
