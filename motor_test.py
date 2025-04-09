import RPi.GPIO as GPIO
import time

MOTOR_PWM_PIN = 12
SERVO_PWM_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PWM_PIN, GPIO.OUT)
GPIO.setup(SERVO_PWM_PIN, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz (20ms period)
motor_pwm = GPIO.PWM(MOTOR_PWM_PIN, 50)
servo_pwm = GPIO.PWM(SERVO_PWM_PIN, 50)

motor_pwm.start(7.5)
servo_pwm.start(7.5)
time.sleep(1)

# Define motor min/max/neutral duty cycles
MOTOR_MIN_DUTY = 5      # Full reverse (1ms pulse)
MOTOR_NEUTRAL_DUTY = 7.5  # Stop (1.5ms pulse)
MOTOR_MAX_DUTY = 10     # Full forward (2ms pulse)
MOTOR_STEP = 0.05
MOTOR_DELAY = 0.05

# Define servo duty cycle limits
SERVO_MIN_DUTY = 2.5   # 0° (500us)
SERVO_NEUTRAL_DUTY = 7.5  # 90° (1500us)
SERVO_MAX_DUTY = 12.5  # 180° (2500us)

current_motor_duty = MOTOR_NEUTRAL_DUTY
current_servo_duty = SERVO_NEUTRAL_DUTY

motor_pwm.ChangeDutyCycle(current_motor_duty)

current_motor_duty = MOTOR_NEUTRAL_DUTY + MOTOR_STEP
motor_pwm.ChangeDutyCycle(current_motor_duty)


try:
    while True:
        user_input = input("Enter 'f' (forward), 'b' (backward), 's' (stop), 'l' (left), 'r' (right), 'c' (center), or 'q' (quit): ").strip().lower()

        if user_input.startswith("f"):  # Forward acceleration
            while current_motor_duty < MOTOR_MAX_DUTY:
                current_motor_duty = min(current_motor_duty + MOTOR_STEP, MOTOR_MAX_DUTY)
                motor_pwm.ChangeDutyCycle(current_motor_duty)
                time.sleep(MOTOR_DELAY)

        elif user_input.startswith("b"):  # Reverse acceleration
            while current_motor_duty > MOTOR_MIN_DUTY:
                current_motor_duty = max(current_motor_duty - MOTOR_STEP, MOTOR_MIN_DUTY)
                motor_pwm.ChangeDutyCycle(current_motor_duty)
                time.sleep(MOTOR_DELAY)

        elif user_input.startswith("s"):  # Smooth stop
            while round(current_motor_duty, 2) != MOTOR_NEUTRAL_DUTY:
                current_motor_duty += MOTOR_STEP if current_motor_duty < MOTOR_NEUTRAL_DUTY else -MOTOR_STEP
                motor_pwm.ChangeDutyCycle(current_motor_duty)
                time.sleep(MOTOR_DELAY)

        elif user_input.startswith("l"):  # Turn Left (0°)
            current_servo_duty = SERVO_MIN_DUTY
            servo_pwm.ChangeDutyCycle(current_servo_duty)
            print("Turning left...")

        elif user_input.startswith("r"):  # Turn Right (180°)
            current_servo_duty = SERVO_MAX_DUTY
            servo_pwm.ChangeDutyCycle(current_servo_duty)
            print("Turning right...")

        elif user_input.startswith("c"):  # Center steering (90°)
            current_servo_duty = 7.5  # 90° position (1.5ms pulse)
            servo_pwm.ChangeDutyCycle(current_servo_duty)
            print("Steering centered.")

        elif user_input.startswith("q"):  # Quit
            print("Exiting motor and servo control...")
            break

        else:
            print("Invalid input. Use 'f' (forward), 'b' (backward), 's' (stop), 'l' (left), 'r' (right), 'c' (center), or 'q' (quit).")

except KeyboardInterrupt:
    print("\nExiting gracefully...")

finally:
    motor_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()
    print("GPIO Cleaned Up.")