import numpy as np
import pyaudio

# Audio settings
SAMPLE_RATE = 44100  # Standard sample rate for audio (44.1 kHz)
FREQ = 40  # Target sine wave frequency (40 Hz)
DURATION = 10  # Play for 10 seconds
AMPLITUDE = 300 / 2000  # Scale for 300mVpp if the default output is ~2Vpp

# Generate sine wave
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
wave = (AMPLITUDE * np.sin(2 * np.pi * FREQ * t)).astype(np.float32)

# Initialize audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True)

# Play sine wave
stream.write(wave.tobytes())

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()

