import time
import board
import busio
import math
import adafruit_mcp4725

# Initialize I2C and MCP4725 DAC
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)


# Test output voltages
dac.raw_value = 0       # Should output ~0V
input("Press Enter to continue...")
dac.raw_value = 2048    # Should output ~1.65V (if VREF = 3.3V)
input("Press Enter to continue...")
dac.raw_value = 4095    # Should output ~3.3V (if VREF = 3.3V)
input("Press Enter to continue...")