import time
import board
import busio
import math
import adafruit_mcp4725

# Initialize I2C and MCP4725 DAC
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)

# Sine wave settings
FREQ = 40  # Target sine wave frequency (Hz)
SAMPLERATE = 5000  # Number of samples per second (higher = smoother)
STEPS = 100  # Steps per sine wave cycle

# Scaling to 300mV peak-to-peak
VREF = 3.3  # MCP4725 is powered at 3.3V
V_CENTER = 1.65  # Center voltage (neutral)
V_PEAK = 0.15  # 150mV peak (total 300mVpp)

# Convert voltages to DAC values
DAC_MAX = int((V_CENTER + V_PEAK) / VREF * 4095)
DAC_MIN = int((V_CENTER - V_PEAK) / VREF * 4095)

# Generate sine wave values scaled between DAC_MIN and DAC_MAX
sine_wave = [
    int(DAC_MIN + (DAC_MAX - DAC_MIN) * (math.sin(2 * math.pi * i / STEPS) + 1) / 2)
    for i in range(STEPS)
]

# Output sine wave continuously
try:
    while True:
        for value in sine_wave:
            dac.raw_value = value  # Send value to DAC
            time.sleep(1 / SAMPLERATE)  # Control waveform smoothness
except KeyboardInterrupt:
    print("\nExiting...")
