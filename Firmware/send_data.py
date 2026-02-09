from os import getenv
import ipaddress
import wifi
import socketpool
import adafruit_requests
import adafruit_connection_manager

import time
import board
import busio
import adafruit_veml7700
import adafruit_ahtx0


# Get WiFi details, ensure these are setup in settings.toml
ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")

if None in [ssid, password]:
    raise RuntimeError(
        "WiFi settings are kept in settings.toml, "
        "please add them there. The settings file must contain "
        "'CIRCUITPY_WIFI_SSID', 'CIRCUITPY_WIFI_PASSWORD', "
        "at a minimum."
    )

print()
print("Connecting to WiFi")

#  connect to your SSID
try:
    wifi.radio.connect(ssid, password)
except TypeError:
    print("Could not find WiFi info. Check your settings.toml file!")
    raise

print("Connected to WiFi")



# Initialize Wifi, Socket Pool, Request Session

# HTTP connections - client and server introduce themselves.
# HTTP requests - client asking for something from server.

# pool: basically, you have a bunch of predefined sockets, if one is unavailable, another one is used. This is a standard practice
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
print("pool created")

# ssl_context: for making secure HTTPS requests.
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
print("ssl context created")

# requests: Initializes a session for making HTTP requests, using the socket pool and SSL contex
requests = adafruit_requests.Session(pool, ssl_context)
print("request created")

url = "http://192.168.1.66:5000/uploads"


i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040, RP2350
veml7700 = adafruit_veml7700.VEML7700(i2c)
aht20 = adafruit_ahtx0.AHTx0(i2c)

while True:
    try:
        temperature = aht20.temperature
        humidity = aht20.relative_humidity
        light_ambient = veml7700.light
        light_lux = veml7700.lux
 
        # prepare dato to send
        data = {"temperature": temperature, "humidity": humidity,
                "light_ambient": light_ambient, "light_lux": light_lux}
        print("sending:", data)
        
        # send JSON with correct header
        response = requests.post(
            url,
            json=data,
        )

        print("Response:", response.status_code, "Body:", response.text)
        response.close()
        
    
        time.sleep(60)
    
    except Exception as e:
        print("Error:", e)
        time.sleep(5)