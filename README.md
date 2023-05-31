# Raspberry remote shutdown
 

 - [Video Tutorial](https://youtu.be/WR0WdTBQJGo)   
 - [Original repo](https://github.com/SensorsIot/Raspberry-remote-shutdown)   

## Resources

- [D2XX Drivers - FTDI](https://ftdichip.com/drivers/d2xx-drivers/)
- [Sonoff – $5 WiFi Wireless Smart Switch Introduction](https://randomnerdtutorials.com/sonoff-5-wifi-wireless-smart-switch-introduction/)
- [How to Flash a Custom Firmware to Sonoff](https://randomnerdtutorials.com/how-to-flash-a-custom-firmware-to-sonoff/)
- [Reprogram Sonoff Smart Switch with Web Server](https://randomnerdtutorials.com/reprogram-sonoff-smart-switch-with-web-server/)
- [Install Mosquitto MQTT Broker on Raspberry Pi](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/)
- [Testing Mosquitto Broker and Client on Raspberry Pi](https://randomnerdtutorials.com/testing-mosquitto-broker-and-client-on-raspbbery-pi/)
- [Using ESPHome With Sonoff Basic](https://esphome.io/devices/sonoff_basic.html)
- [Buck converters: Quieten your 3D printer with a Noctua fan & directly power your Pi](https://www.youtube.com/watch?v=yW9ovo9CHi0)

## Installation 

Use Raspberry Pi Imager to install on the microSD the Raspbian OS with preinstalled Octoprint

Ssh into the Raspberry Pi, if you kept the default settings you just will   
``` ssh octoprint@octopi.local ```

To install everything via install.sh download the folder and ``` cd ``` into it:   
``` cd /home/pi/raspberry-remote-shutdown ``` 

Install desktop environment to use VNC  
`sudo /home/octoprint/scripts/install-desktop `

Install vnc  
` sudo apt install realvnc-vnc-server realvnc-vnc-viewer `

Set Desktop gui to boot at startup and set the resolution at least at 1280 x 720   
` sudo raspi-config `

Install Chromium   
`sudo apt-get install chromium-browser --yes `

Make the script executable:   
``` chmod +x install.sh ```   

Run the script:    
``` sudo ./install.sh ```   

## Testing MQTT

From terminal send MQTT messages to the broker which sends them to ESPHome client.    

To turn on:   
``` mosquitto_pub -d -t ender/switch/mains/command -m "on" ```   

To turn off:   
``` mosquitto_pub -d -t ender/switch/mains/command -m "off" ```   

To turn off after 30 seconds delay:   
``` mosquitto_pub -d -t ender/mains -m "off" ```   

