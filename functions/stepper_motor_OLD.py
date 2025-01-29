from time import sleep
import pigpio

def stop():
    pi = pigpio.pi()

    STEP = 17
    SLP = 15

    #pi.set_PWM_frequency(STEP, 0)
    pi.set_PWM_dutycycle(STEP, 0)

    pi.write(SLP, 0)

# NOTE:
# DIR = Direction GPIO Pin
# STEP = Step GPIO Pin
# SLP = Sleep Pin
# SWITCH is NOT used.
# MODE = Microstep Resolution GPIO Pins
def raise_window(speed: int = 0) -> None:
    if speed <= 0 or speed >= 3:
        raise Exception("Speed was not passed into motor_runner or is an invalid input!")
    
    # EDIT THESE LATER
    DIR = 2     # Direction GPIO Pin
    STEP = 17    # Step GPIO Pin
    SLP = 15
    #SWITCH = 16  # GPIO pin of switch
    
    # Clockwise and Counter-Clockwise
    CW = 1
    CCW = 0

    # Connect to pigpiod daemon
    pi = pigpio.pi()

    # Set up pins as an output
    pi.set_mode(DIR, pigpio.OUTPUT)
    pi.set_mode(STEP, pigpio.OUTPUT)

    # Set up input switch
    # pi.set_mode(SWITCH, pigpio.INPUT)
    # pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)

    # EDIT MODE LATER
    MODE = (3, 4, 14)   # Microstep Resolution GPIO Pins
    RESOLUTION = {'Full': (0, 0, 0),
                'Half': (1, 0, 0),
                '1/4': (0, 1, 0),
                '1/8': (1, 1, 0),
                '1/16': (0, 0, 1),
                '1/32': (1, 0, 1)}

    for i in range(3):
        pi.write(MODE[i], RESOLUTION['Full'][i])

    pi.write(SLP, 1)

    # Set duty cycle and frequency

    # SOFTWARE PWM

    pi.set_PWM_dutycycle(STEP, 128)  # PWM 1/2 On 1/2 Off

    # USE FREQUENCY FOR SPEED, NOT DUTY CYCLE!
    pi.set_PWM_frequency(STEP, 1000)  # 500 pulses per second

    # HARDWARE PWM (not working?)

    #pi.hardware_PWM(STEP, 500, 128)

    while True:
        pi.write(DIR, CW)
        sleep(1)
        pi.write(DIR, CCW)
        sleep(1)

    pi.set_PWM_dutycycle(STEP, 0)

    pi.write(SLP, 0)

    pi.stop()


# NOTE:
# DIR = Direction GPIO Pin
# STEP = Step GPIO Pin
# SLP = Sleep Pin
# SWITCH is NOT used.
# MODE = Microstep Resolution GPIO Pins
def lower_window(speed: int = 0) -> None:
    if speed <= 0 or speed >= 3:
        raise Exception("Speed was not passed into motor_runner or is an invalid input!")
    
    # EDIT THESE LATER
    DIR = 2     # Direction GPIO Pin
    STEP = 17    # Step GPIO Pin
    SLP = 15
    #SWITCH = 16  # GPIO pin of switch
    
    # Clockwise and Counter-Clockwise
    CW = 1
    CCW = 0

    # Connect to pigpiod daemon
    pi = pigpio.pi()

    # Set up pins as an output
    pi.set_mode(DIR, pigpio.OUTPUT)
    pi.set_mode(STEP, pigpio.OUTPUT)

    # Set up input switch
    # pi.set_mode(SWITCH, pigpio.INPUT)
    # pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)

    # EDIT MODE LATER
    MODE = (3, 4, 14)   # Microstep Resolution GPIO Pins
    RESOLUTION = {'Full': (0, 0, 0),
                'Half': (1, 0, 0),
                '1/4': (0, 1, 0),
                '1/8': (1, 1, 0),
                '1/16': (0, 0, 1),
                '1/32': (1, 0, 1)}

    for i in range(3):
        pi.write(MODE[i], RESOLUTION['Full'][i])

    pi.write(SLP, 1)

    # Set duty cycle and frequency

    # SOFTWARE PWM

    pi.set_PWM_dutycycle(STEP, 128)  # PWM 1/2 On 1/2 Off

    # USE FREQUENCY FOR SPEED, NOT DUTY CYCLE!
    pi.set_PWM_frequency(STEP, 1000)  # 500 pulses per second

    # HARDWARE PWM (not working?)

    #pi.hardware_PWM(STEP, 500, 128)

    while True:
        pi.write(DIR, CW)
        sleep(1)
        pi.write(DIR, CCW)
        sleep(1)

    pi.set_PWM_dutycycle(STEP, 0)

    pi.write(SLP, 0)

    pi.stop()
