#!/bin/bash
echo "Shutdown started"
mosquitto_pub -h octopi.local -t ender/mains -m "off"
sudo shutdown now
