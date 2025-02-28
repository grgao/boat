import RPi.GPIO as GPIO
import time

PWM_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz (20ms period)
pwm = GPIO.PWM(PWM_PIN, 50)
pwm.start(7.5)

try:
    while True:
        user_input = input("Enter 'f' for forward, 'b' for backward, 's' to stop, or 'q' to quit: ").lower()
        
        if user_input == "f":
            pwm.ChangeDutyCycle(10)  # 2ms pulse (Full forward)
            print("Thruster: Moving Forward")

        elif user_input == "b":
            pwm.ChangeDutyCycle(5)  # 1ms pulse (Full backward)
            print("Thruster: Moving Backward")

        elif user_input == "s":
            pwm.ChangeDutyCycle(7.5)  # 1.5ms pulse (Neutral Stop)
            print("Thruster: Stopped")

        elif user_input == "q":
            break  # Exit loop and cleanup
        
        else:
            print("Invalid input. Use 'f' (forward), 'b' (backward), 's' (stop), or 'q' (quit).")

except KeyboardInterrupt:
    print("\nPWM Stopped.")

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO Cleaned Up.")