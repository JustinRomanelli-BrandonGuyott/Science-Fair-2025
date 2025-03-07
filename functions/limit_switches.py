from multiprocessing import Process
from functions.stepper_motor import stop
import RPi.GPIO as GPIO
import time


# Needed to provide a bool to prevent window from opening into itself.
def write_can_move_up(can_move):
    with open("./can_move_up.txt", "w+") as f_cmu:
        f_cmu.write(str(can_move))
        f_cmu.close()

def write_can_move_down(can_move):
    with open("./can_move_down.txt", "w+") as f_cmd:
        f_cmd.write(str(can_move))
        f_cmd.close()


def write_time():
    with open("./time.txt", "r") as f:
        f.seek(0)
        init_time = float(f.read())
        f.close()
    
    with open("./final_time.txt", "w+") as f:
        f.seek(0)
        f.write(str(time.time() - init_time))
        f.close()
        

def LS_watchdog():
    p_ls = Process(target=LS_check, args=((6, 5), (24, 25)))
    p_ls.start()
    return p_ls


# NOTE: in pins_upper and pins_lower, the first int is the INPUT and the second is the OUTPUT.
def LS_check(pins_upper: tuple[int, int], pins_lower: tuple[int, int]):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Top limit switch
    GPIO.setup(pins_upper[0], GPIO.IN)
    GPIO.setup(pins_upper[1], GPIO.OUT)

    # Bottom Limit Switch
    GPIO.setup(pins_lower[0], GPIO.IN)
    GPIO.setup(pins_lower[1], GPIO.OUT)

    # Initialize current in output wires
    GPIO.output(pins_upper[1], 0)
    GPIO.output(pins_lower[1], 0)

    
    while (True):
        if GPIO.input(pins_upper[0]):
            stop()
            write_time()
            print("Successful Stop: Upper")
            write_can_move_up(False)
            
            while (True):
                current_readings = []
                for i in range(100000):
                    current_readings.append(GPIO.input(pins_upper[0]))
                if (all(x == 0 for x in current_readings)):
                    write_can_move_up(True)
                    break
        
        elif GPIO.input(pins_lower[0]):
            stop()
            write_time()
            print("Successful Stop: Lower")
            write_can_move_down(False)
            
            while (True):
                current_readings = []
                for i in range(100000):
                    current_readings.append(GPIO.input(pins_lower[0]))
                if (all(x == 0 for x in current_readings)):
                    write_can_move_down(True)
                    break