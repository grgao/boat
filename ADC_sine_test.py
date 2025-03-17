import time
import board
import busio
import math
import adafruit_mcp4725

# Initialize I2C and MCP4725 DAC
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)


dac.raw_value = 2232  # Should be ~1.80V