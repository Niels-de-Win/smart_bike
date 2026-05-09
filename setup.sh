#!/bin/bash

ENV_FILE=~/Smart_Bike/.env

cd ~/Smart_Bike

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
sudo nmcli dev wifi connect "$SSID" password "$WIFI_PASSWORD"
echo "WiFi updated."

echo ""
echo "=== Setup complete. Starting Smart Bike... ==="
echo ""

source .venv/bin/activate
python lock.py
