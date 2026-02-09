# Sleepy Board (v0)

The Sleepy Board can be used to capture temperature, humidity and brightness data. Data is read from sensors connected to a microcontroller, which is then transmitted to a database over wifi. I live right next to a main road and wanted to know what my room looks like once I have fallen asleep.

This version, my latest weekend project, is a prototype. The aim of this exercise is to see how quickly I can get a system up and running using all the off the shelf bits of hardware and electronics I can find. the firmware was the easier part - thanks to guides and libraries from Adafruit. The HTML files were generated using AI.

## Connecting the hardware
I have a RaspberryPi Pico 2W connected to the following sensors on the same I2C bus.

| Sensor             | Part number | I2C Addr | Reference links    |
|--------------------|-------------|----------|--------------------|
|Temperaure, Humidity| AHT20       | 0x38     | [link](https://learn.adafruit.com/adafruit-aht20) |
|Brightness          | VEML7700    | 0x10     | [link](https://learn.adafruit.com/adafruit-veml7700) |

| Signal  | Pin on Pico | Ref. colours|
|---------|-------------|-------------|
| I2C_SDA | GP0         | Blue        |
| I2C_SCL | GP1         | Yellow      |


## Setting up the Pico
Using circuitpython since it is, in my opinion, the easiest to use. I am using [CircuitPython 10.0.3](https://circuitpython.org/board/raspberry_pi_pico2_w/), which is the latest at the time of writing this. There are multiple files  in the Firmware folder.

- I2C scanner: Scan all the I2C addresses and list connected devices.
- Read sensor data: More information can be found in the individual .py file.
- Basic Wifi Test: [This](https://learn.adafruit.com/pico-w-wifi-with-circuitpython/pico-w-basic-wifi-test) is a quick guide from Adafruit on how to get the Pico to connect to the internet. Don't forget to update `settings.toml` with the correct Wifi SSID and password. 
- These two files and then combined into another script that is used to send data to the server.

## Setting up the server
I used flask to set up a server on my laptop. To run the server:

```
cd Software/flask_server
source venv/bin/activate

# Install packages if needed
pip install some-package

# Run app
flask --app app_server run --host=0.0.0.0 --port=5000

# Stop working
deactivate
flask --app app_server run --host=0.0.0.0 --port=5000
```


Things to keep in mind:
1. Identical JSON formats on the server and the Pico
2. Correct URL on the Pico (use `ifconfig` to find the IP address of the device the Pico needs to talk to)
3. Don't `break` when you see an Exception - keep trying.


## How to run everything!
1. Run the flask server 
2. Transfer the files in the Firmware folder onto the Pico. Start sending data.
3. Open the correct address on a web browser conencted to any device on the same wifi network et voilà !