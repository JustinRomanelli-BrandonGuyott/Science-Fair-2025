import pigpio
import time
from functions.emergency_stop import led_moving, led_stopped

# DRV8825 PIN INITIALIZATION
DIR = 2     # Direction GPIO Pin
STEP = 17   # Step GPIO Pin
SLP = 15    # Sleep GPIO Pin (turns driver off)

# Clockwise and Counter-Clockwise direction variables
down = 1
up = 0

# Establish connection to pigpiod daemon
pi = pigpio.pi()

def setup_motors() -> None:
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
    pi.set_PWM_frequency(STEP, 800)  
    pi.write(SLP, 0)



def safe_to_close():
    with open("./safe_to_close.txt", "r") as safety_file:
        status = safety_file.read()
        safety_file.close()
    if status == "True":
        return True
    elif status == "False":
        return False

def can_move_down():
    with open("./can_move_down.txt", "r") as cmd_file:
        status = cmd_file.read()
        cmd_file.close()
    if status == "True":
        return True
    elif status == "False":
        return False

def can_move_up():
    with open("./can_move_up.txt", "r") as cmu_file:
        status = cmu_file.read()
        cmu_file.close()
    if status == "True":
        return True
    elif status == "False":
        return False

# DEPRECATED
def set_frequency(frequency) -> None:
    pi.set_PWM_frequency(STEP, frequency)  

def power_on() -> None:
    if (pi.read(DIR)):
        direction = "down"
    elif (not(pi.read(DIR))):
        direction = "up"

    if (not(can_move_up()) and direction == "up"):  # Prevents from going up when fully opened
        print("ERROR: Cannot move further up.")
    elif (not(can_move_down()) and direction == "down"): # Prevents from going down when fully closed
        print("ERROR: Cannot move further down.")
    elif (not(safe_to_close()) and direction == "down"): # Prevents from going down if an object is in the way
        print("ERROR: Object in the way of closing.")
    else:
        if not(pi.read(SLP)):   # This is to prevent multiple power on commands at the same time
            led_moving()
            pi.write(SLP, 1)
            pi.set_PWM_frequency(STEP, 800)
            pi.set_PWM_dutycycle(STEP, 128)
            print("P-ON")


def stop() -> None:
    pi.set_PWM_dutycycle(STEP, 0)
    pi.set_PWM_frequency(STEP, 0)
    pi.write(SLP, 0)
    print("P-OFF")
    led_stopped()


def open_window() -> None:
    pi.write(DIR, up)
    print("Opening   window...")
    power_on()

    with open("./time.txt", "w") as f:
        f.seek(0)
        f.write(str(time.time()))
        f.close()

        #start_time = time.time()
        #while not(pi.read(6)):
        #    pass
        #stop()
        #end_time = time.time()
        #delta_time = end_time - start_time
        #with open("./time.txt", "w+") as f:
        #    f.write(str(delta_time))
        # Rewrite calculated time using a different script
        # Start it here, log into a file
        # In LS Process, when limit switch is pressed log time
        # Then calculate delta time
    
    
def close_window() -> None:
    pi.write(DIR, down)
    print("Closing window...")
    power_on()

    with open("./time.txt", "w") as f:
        f.seek(0)
        f.write(str(time.time()))
        f.close()

        #start_time = time.time()
        #with open("./time.txt", "w+") as f:
        #    f.write(str(start_time))


        # NOTE: FOR LIMIT SWITCH CODE

        #end_time = time.time()
        #delta_time = end_time - start_time
        #with open("./time.txt", "w+") as f:
        #    f.write(str(delta_time))
        # SEE ABOVE FOR PLANNED ALGORITHM