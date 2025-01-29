import pigpio
import time


# DRV8825 
DIR = 2     # Direction GPIO Pin
STEP = 17   # Step GPIO Pin
SLP = 15    # Sleep GPIO Pin (turns driver off)

# Clockwise and Counter-Clockwise
down = 1
up = 0

# Establish connection to pigpiod daemon
pi = pigpio.pi()


def setup_motors() -> None:
    pi = pigpio.pi()

    # Microstep Resolution GPIO Pins
    MODE = (3, 4, 14)
    RESOLUTION = {'Full': (0, 0, 0),
                'Half': (1, 0, 0),
                '1/4': (0, 1, 0),
                '1/8': (1, 1, 0),
                '1/16': (0, 0, 1),
                '1/32': (1, 0, 1)}

    for i in range(3):
        pi.write(MODE[i], RESOLUTION['Full'][i])

    # Sets the DRV8825 driver into an off position by default
    pi.write(SLP, 0)


def set_frequency(frequency) -> None:
    pi.set_PWM_frequency(STEP, frequency)  

def power_on() -> None:
    pi.write(SLP, 1)
    pi.set_PWM_dutycycle(STEP, 128)
    print("P-ON")


def stop() -> None:
    pi.set_PWM_dutycycle(STEP, 0)
    pi.write(SLP, 0)
    print("P-OFF")


def open_window() -> None:
    if not(pi.read(6)):   
        pi.write(DIR, up)
        power_on()

        start_time = time.time()

        
        while not(pi.read(6)):
            pass
        stop()
        end_time = time.time()
        delta_time = end_time - start_time
        with open("./time.txt", "w+") as f:
            f.write(str(delta_time))
        
    
def close_window() -> None:
    if not(pi.read(24)):
        pi.write(DIR, down)
        power_on()

        start_time = time.time()

        while not(pi.read(24)):
            pass
        stop()

        end_time = time.time()
        delta_time = end_time - start_time
        with open("./time.txt", "w+") as f:
            f.write(str(delta_time))    #p_ls = limit_switch_watchdog()
