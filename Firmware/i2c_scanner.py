# A modified version of:

# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython I2C Device Address Scan"""

import time
import board
import busio

i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040, RP2350

while not i2c.try_lock():
    pass

try:
    print(
        "I2C addresses found:",
        [hex(device_address) for device_address in i2c.scan()],
    )
    time.sleep(1)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()
