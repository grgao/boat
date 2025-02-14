import RPi.GPIO as GPIO
import time

PWM_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz (20ms period)
pwm = GPIO.PWM(PWM_PIN, 50)
pwm.start(5)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("stopped")