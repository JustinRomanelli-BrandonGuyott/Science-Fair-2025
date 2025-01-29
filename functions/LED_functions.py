import RPi.GPIO as GPIO

# GPIO pins for the LEDs.

RED = 27
GREEN = 22
YELLOW = 10

# All of the functions below are for shorthand use to turn on or off an individual LED light.

def red_led_on() -> None:

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(RED, GPIO.OUT)
    
    GPIO.output(RED, True)

def red_led_off() -> None:

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(RED, GPIO.OUT)
    
    GPIO.output(RED, False)

def yellow_led_on() -> None:

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(YELLOW, GPIO.OUT)
    
    GPIO.output(YELLOW, True)

def yellow_led_off() -> None:

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(YELLOW, GPIO.OUT)
    
    GPIO.output(YELLOW, False)

def green_led_on() -> None:

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(GREEN, GPIO.OUT)

    GPIO.output(GREEN, True)

def green_led_off() -> None:

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(GREEN, GPIO.OUT)

    GPIO.output(GREEN, False)