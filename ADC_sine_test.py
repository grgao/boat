import time
import board
import busio
import math
import adafruit_mcp4725
#this board has a working voltage of 2.7 ~ 5.5V

# Set up I2C communication (I think, not sure, google said this)
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)  # MCP4725 address

dac.raw_value = 2048