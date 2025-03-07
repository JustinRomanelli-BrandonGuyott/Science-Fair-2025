#from LED_functions import red_led_on, red_led_off, green_led_on, green_led_off, yellow_led_off, yellow_led_on
from functions.LED_functions import red_led_on, red_led_off, green_led_on, green_led_off, yellow_led_off, yellow_led_on
import pigpio

# Connect to PiGPIO daemon
pi = pigpio.pi()

SLP = 15

def emergency_stop(should_stop: bool = True) -> None:

    if should_stop:
        print("Emergency Stop")

        # Variables for Step and Sleep pins
        STEP = 17

        # Turn off the motor.
        pi.set_PWM_dutycycle(STEP, 0)

        pi.write(SLP, 0)

        green_led_off()

        yellow_led_off()

        red_led_on()
    else:
        led_stopped()


def led_moving() -> None:
    green_led_off()
    red_led_off()
    yellow_led_on()


def led_stopped() -> None:
    if not(pi.read(SLP)):
        green_led_on()
        red_led_off()
        yellow_led_off()
