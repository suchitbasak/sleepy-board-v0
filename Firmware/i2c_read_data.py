# Reading sensor data

"""
To get data from the VEML7700 light sensor, install the following:
- adafruit_bus_device
- adafruit_register
- adafruit_veml7700.mpy

To get data from the AHT20 temp & humidity sensor, install the following:
- adafruit_bus_device (already added above)
- adafruit_ahtx0.mpy

library files can be donwloaded from:
from: https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases
"""

import time
import board
import busio
import adafruit_veml7700
import adafruit_ahtx0

i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040, RP2350
veml7700 = adafruit_veml7700.VEML7700(i2c)
aht20 = adafruit_ahtx0.AHTx0(i2c)

while True:
    print("Ambient light:", veml7700.light)
    print("Lux:", veml7700.lux)
    print("Temp:", aht20.temperature)
    print("Humidity:", aht20.relative_humidity)
    print("-------------------------------")
    time.sleep(5)