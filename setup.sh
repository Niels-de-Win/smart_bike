#!/bin/bash

ENV_FILE=".env"

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Ask for network settings
echo "=== Smart Bike Setup ==="
echo ""
read -p "WiFi network name (SSID): " SSID
read -s -p "WiFi password: " WIFI_PASSWORD
echo ""
read -p "Phone IP address (e.g. 192.168.1.22): " PHONE_IP

# Save to .env file
cat > $ENV_FILE <<EOF
SSID=$SSID
WIFI_PASSWORD=$WIFI_PASSWORD
PHONE_IP=$PHONE_IP
EOF

echo ""
echo "Settings saved to .env"

# Apply WiFi settings
if command -v nmcli &> /dev/null; then
    sudo nmcli dev wifi connect "$SSID" password "$WIFI_PASSWORD"
    echo "WiFi updated."
else
    echo "Warning: nmcli not found. Please update WiFi manually."
fi

# Setup virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Installing requirements..."
source .venv/bin/activate
pip install -r requirements.txt

echo ""
echo "=== Setup complete. Starting Smart Bike... ==="
echo ""

python3 lock.py

