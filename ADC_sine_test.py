import time
import math
import board
import busio
import adafruit_mcp4725

# Initialize I2C and MCP4725 DAC
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)

# Sine wave parameters
FREQ = 40  # 40 Hz sine wave
SAMPLERATE = 5000  # Must be much higher than 40Hz for smooth output
STEPS = 100  # Number of steps per cycle

# Full DAC range (0 to 4095) for 3.3Vpp
DAC_MAX = 4095  # 3.3V
DAC_MIN = 0     # 0V

# Generate sine wave lookup table (from 0V to 3.3V)
sine_wave = [
    int(DAC_MIN + (DAC_MAX - DAC_MIN) * (math.sin(2 * math.pi * i / STEPS) + 1) / 2)
    for i in range(STEPS)
]

# Output sine wave continuously
try:
    while True:
        for value in sine_wave:
            dac.raw_value = value  # Send value to DAC
            time.sleep(1 / (SAMPLERATE))  # Control smoothness
except KeyboardInterrupt:
    print("\nExiting...")
