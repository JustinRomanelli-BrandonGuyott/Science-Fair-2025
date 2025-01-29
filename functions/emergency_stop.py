from functions.LED_functions import red_led_on, red_led_off, green_led_on, green_led_off, yellow_led_off, yellow_led_on
import pigpio

# Connect to PiGPIO daemon
pi = pigpio.pi()

# Stops the motor directly by cutting power to the motor.
# Also turns off the green and yellow LED lights, and turns on the red LED light.
def emergency_stop(should_stop: bool = True) -> None:

    if should_stop:
        print("Emergency Stop")

        # Variables for Step and Sleep pins
        STEP = 17

        SLP = 15

        # Turn off the motor.
        pi.set_PWM_dutycycle(STEP, 0)

        pi.write(SLP, 0)

        # Alter the LEDs such that only the red one is active.
        green_led_off()

        yellow_led_off()

        red_led_on()

# Shorthand methods for LEDs are below.

def led_resume() -> None:
    
    green_led_on()
    red_led_off()
    yellow_led_off()


def led_pause() -> None:

    green_led_off()
    red_led_off()
    yellow_led_on()