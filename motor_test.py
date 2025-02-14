import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz (20ms period)
pwm = GPIO.PWM(12, 50)

# PWM signal with 25% duty cycle
def motor_on():
    pwm.start(25)  # Start PWM with 25% duty cycle
    time.sleep(1.5)  # Keep the motor on for 1.5 seconds
    pwm.stop()  # Stop PWM