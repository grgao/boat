import RPi.GPIO as GPIO
import time
import math

# Set up PWM pin
PWM_PIN = 12  # Use a PWM-capable GPIO pin (e.g., GPIO 18)
FREQ = 1000  # Base PWM frequency (1 kHz)
SINE_FREQ = 40  # Desired sine wave frequency (40 Hz)
STEPS = 100  # Number of steps per sine wave cycle

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

pwm = GPIO.PWM(PWM_PIN, FREQ)  # Initialize PWM
pwm.start(0)  # Start with 0% duty cycle

try:
    while True:
        for i in range(STEPS):
            duty = (math.sin(2 * math.pi * i / STEPS) + 1) * 50  # Normalize to 0-100%
            pwm.ChangeDutyCycle(duty)
            time.sleep(1 / (SINE_FREQ * STEPS))  # Time per step
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

