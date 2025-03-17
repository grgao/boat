import time
import board
import busio
import math
import adafruit_mcp4725
#this board has a working voltage of 2.7 ~ 5.5V

# Set up I2C communication (I think, not sure, google said this)
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)

# DAC settings
VREF = 4095  # 12-bit resolution max value, this will be 3.3V if we use that pin or 5V if we use that one
FREQ = 40  # sine wave frequency (Hz) Idk why the other one output 30 Hz but this might work better
SAMPLERATE = 5000  # Number of samples per second (higher = smoother)
STEPS = 100  # Steps per sine wave cycle

# Precompute sine wave lookup table *check my math pls*
sine_wave = [int((math.sin(2 * math.pi * i / STEPS) + 1) * VREF / 2) for i in range(STEPS)]

# Output the sine wave
try:
    while True:
        for value in sine_wave:
            dac.value = value  # Send value to MCP4725
            time.sleep(1 / SAMPLERATE)  # Adjust update speed
except KeyboardInterrupt:
    print("\nExiting")