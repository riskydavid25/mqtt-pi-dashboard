#!/bin/bash

# Update dan upgrade sistem
sudo apt update && sudo apt upgrade -y

# Instal Mosquitto MQTT Broker
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Instal Python3 dan pip
sudo apt install -y python3 python3-pip

# Instal Flask
pip3 install flask

# Buat direktori untuk proyek
mkdir -p ~/mqtt-dashboard
cd ~/mqtt-dashboard

# Salin file yang diperlukan dari repository
cp ~/mqtt-pi-dashboard/mqtt_logger.py .
cp ~/mqtt-pi-dashboard/mqtt_dashboard_server.py .
mkdir -p templates
cp ~/mqtt-pi-dashboard/templates/index.html templates/

# Jalankan logger MQTT
nohup python3 mqtt_logger.py &

# Jalankan server Flask
nohup python3 mqtt_dashboard_server.py &
