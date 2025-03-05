import RPi.GPIO as GPIO
import time

PWM_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz (20ms period)
pwm = GPIO.PWM(PWM_PIN, 50)
pwm.start(7.5)
time.sleep(1)

# Define min, max, and neutral duty cycle values
MIN_DUTY = 5   # 1ms pulse (Full reverse)
NEUTRAL_DUTY = 7.5  # 1.5ms pulse (Stop)
MAX_DUTY = 10  # 2ms pulse (Full forward)
STEP = 0.05  # How much to increase/decrease per step
DELAY = 0.05  # Time delay per step for smooth throttle

current_duty = NEUTRAL_DUTY

try:
    while True:
        user_input = input("Enter 'f' for forward, 'b' for backward, 's' to stop, or 'q' to quit: ").lower()
        
        if user_input == "f":
            while current_duty < MAX_DUTY:
                current_duty += STEP
                if current_duty > MAX_DUTY:
                    current_duty = MAX_DUTY  # Ensure it doesn't exceed max
                pwm.ChangeDutyCycle(current_duty)
                time.sleep(DELAY)

        elif user_input == "b":
            while current_duty > MIN_DUTY:
                current_duty -= STEP
                if current_duty < MIN_DUTY:
                    current_duty = MIN_DUTY  # Ensure it doesn't go below min
                pwm.ChangeDutyCycle(current_duty)
                time.sleep(DELAY)

        elif user_input == "s":
            while current_duty != NEUTRAL_DUTY:
                if current_duty > NEUTRAL_DUTY:
                    current_duty -= STEP
                    if current_duty < NEUTRAL_DUTY:
                        current_duty = NEUTRAL_DUTY
                else:
                    current_duty += STEP
                    if current_duty > NEUTRAL_DUTY:
                        current_duty = NEUTRAL_DUTY
                
                pwm.ChangeDutyCycle(current_duty)
                time.sleep(DELAY)

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