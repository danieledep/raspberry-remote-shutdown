# Raspberry remote shutdown
 
 - [Video Tutorial](https://youtu.be/WR0WdTBQJGo)   
 - [Original repo](https://github.com/SensorsIot/Raspberry-remote-shutdown)

## Components

- Raspberry Pi 4
- Ender 3
- 2-to-1 XT60 adaptor
- Sonoff Basic RF R2 v1.3
- USB to Serial adapter with FTDI FT232RL chip, like this one: [DSD TECH SH-U09C](https://www.amazon.com/DSD-TECH-Adapter-FT232RL-Compatible/dp/B07BBPX8B8/ref=sr_1_3?crid=T37WPRBNX2BY)
- Momentary switch button

## Installation 

Use **Raspberry Pi Imager** to install on the microSD the Raspbian OS with preinstalled **Octoprint**

Create a new user and login by connecting with a computer in the same network to `http://octopi.local`

After that you will be able to **ssh** into the Raspberry Pi, if you kept the default settings you can just   
`ssh octoprint@octopi.local`

Download the repo from github via https   
`git clone https://github.com/danieledep/raspberry-remote-shutdown.git `

Go into the downloaded folder:   
`cd raspberry-remote-shutdown/ ` 

Make the script executable:   
`chmod +x install.sh `   

Run the script:    
`sudo ./install.sh `  

Install desktop environment to use esphome and nodered on the Raspberry  
`sudo /home/octoprint/scripts/install-desktop `

Set Desktop gui to boot at startup and set the resolution at least at 1280 x 720   
`sudo raspi-config `

Install **Chromium**   
`sudo apt-get install chromium-browser --yes `

Attach a screen, keyboard and mouse to the Raspberry Pi

Install the [D2XX Drivers](https://ftdichip.com/drivers/d2xx-drivers/) for using the FTDI chips from the Raspberry Pi

Go into the project folder:   
`cd raspberry-remote-shutdown/ ` 

> ⚠️ Last time I tryed installing **Esphome** with `pip` it failed to install `cryptography`    
> because of incompatible dependencies, this fixed it:  
> `sudo pip3 install esphome cryptography==3.3.2`

Start up Esphome, use sudo to have write permission for `secrets.yaml`    
`sudo esphome dashboard /config `

Open **Esphome** web ui at `octopi.local:6052`

Press on **Secrets** to save wifi configuration

Create a project name `sonoff` and copy the content of `sonoff.yaml` into the file  

Hit **Save** and then **Install.** 

The first time you flash a new firmware you'll need to connect the Raspberry PI to the Sonoff via the **FTDI Module** wiring the pin like the following diagram. 

```
   FTDI      Sonoff

   GND ----> GND
   VCC ----> 3V3
   TXD ----> RX
   RXD ----> TX   
```

The first time you flash a new firmware you'll also need to keep pressed the physical button of the Sonoff. 

> ⚠️ Newer Raspberry Pi with installed 64bit OS might need to disable temporarely the 64 bit capabilities at boot time, in order to compile the binaries due to compatibility issues with Platformio tooling. To do so edit the `config.txt` :  
> ` sudo nano /boot/config.txt`   
> add to the part titled `[pi4]` a new line like this
> ```
> [pi4]   
> arm_64bit=0 
> ```

Open **NodeRED** at `octopi.local:1880` import our flow `nodered-flow.json` and click **Deploy**

Finally let's enable remote access to the **MQTT broker** without requiring authentication. Open the configuration file  
`sudo nano /etc/mosquitto/mosquitto.conf`   
At the end of the file add these two lines:  
```
listener 1883 
allow_anonymous true
```
 save the file and restart Mosquitto for the changes to take effect.   
`sudo systemctl restart mosquitto`   

Open Octoprint, install the **MQTT** plugin, tick **Activate event messages**, and let's only keep **Printing events** messages enabled.   
Add `octopi.local` as the Broker host.

> ⚠️ By default the plugin has the **Enable retain flag** option checked. This is normally the preferred choice but for our setup where the broker shut itself down multiple times, we don't want to have our server turn on and find retained messages from the previous session. 
 
### Notes

Since I'm running the MQTT Broker directly on the same Raspberry PI that runs Octoprint too, which effectively self-shutdown, I don't need to run the **systemd service**  `shutdown.service`. The service was used by the original author to listen for the MQTT message coming from a different server running the MQTT Broker telling the Raspberry PI running Octoprint to shutdown. But since they both run on the same device I can simply run the **Exec** node from within Node-RED, which upon receiving the `octoprint/shutodwn` MQTT message, it launches the command `sudo shutdown now` to the OS. I still have an updated version of the necessary files and Node-RED nodes in this repository, in case I wanted to change my setup in the future.


### Testing MQTT

Check the **systemd** services are enabled and running   
`systemctl list-unit-files`

From terminal send MQTT messages to the NodeRED client which sends them to the Sonoff.    

To turn on:   
``` mosquitto_pub -d -t sonoff/switch/mains/command -m "on" ```   

To turn off:   
``` mosquitto_pub -d -t sonoff/switch/mains/command -m "off" ```   

To turn off after 30 seconds delay:   
``` mosquitto_pub -d -t sonoff/mains -m "off" ```     

To read log messages from NodeRED in real-time   
`node-red-log`

To read Mosquitto logs file    
`sudo cat /var/log/mosquitto/mosquitto.log`

To read NodeRED logs file    
`sudo cat /var/log/syslog`

### Resources

- [D2XX Drivers - FTDI](https://ftdichip.com/drivers/d2xx-drivers/)
- [Sonoff – $5 WiFi Wireless Smart Switch Introduction](https://randomnerdtutorials.com/sonoff-5-wifi-wireless-smart-switch-introduction/)
- [How to Flash a Custom Firmware to Sonoff](https://randomnerdtutorials.com/how-to-flash-a-custom-firmware-to-sonoff/)
- [Reprogram Sonoff Smart Switch with Web Server](https://randomnerdtutorials.com/reprogram-sonoff-smart-switch-with-web-server/)
- [Install Mosquitto MQTT Broker on Raspberry Pi](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/)
- [Testing Mosquitto Broker and Client on Raspberry Pi](https://randomnerdtutorials.com/testing-mosquitto-broker-and-client-on-raspbbery-pi/)
- [Using ESPHome With Sonoff Basic](https://esphome.io/devices/sonoff_basic.html)
- [GPIO Binary Sensor](https://esphome.io/components/binary_sensor/gpio.html)
- [Buck converters: Quieten your 3D printer with a Noctua fan & directly power your Pi](https://www.youtube.com/watch?v=yW9ovo9CHi0)
 

