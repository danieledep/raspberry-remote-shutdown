#!/bin/bash
echo "Shutdown started"
mosquitto_pub -h octopi.local -t sonoff/mains -m "off"
sudo shutdown now
