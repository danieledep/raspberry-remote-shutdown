#!/bin/bash
echo "installing pip3 - esphome - mosquitto - nodered"
sudo apt update
sudo apt upgrade
sudo apt install python-pip
sudo pip install tornado esptool
sudo pip3 install esphome
sudo apt install -y mosquitto mosquitto-clients
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)

echo "installing services"

sudo systemctl enable nodered.service
sudo cp shutdown.service /etc/systemd/system/shutdown.service
sudo systemctl enable shutdown.service
sudo systemctl start shutdown.service
