import pigpio
import time


# DRV8825 
DIR = 2     # Direction GPIO Pin
STEP = 17   # Step GPIO Pin
SLP = 15    # Sleep GPIO Pin (turns driver off)

# Clockwise and Counter-Clockwise rotation, corresponding to down and up.
down = 1
up = 0

# Establish connection to pigpiod daemon
pi = pigpio.pi()

# Sets up the motors.
def setup_motors() -> None:
    pi = pigpio.pi()

    # Microstep Resolution GPIO Pins
    # Although these pins are not used outside of here, this allows for the gradual opening / closing of the window.
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


# Sets the frequency of the motor.
# Only the frequencies 800 and 1000 are used.
def set_frequency(frequency) -> None:
    pi.set_PWM_frequency(STEP, frequency)  


# Provides power to the stepper motors, allowing them to move.
def power_on() -> None:
    pi.write(SLP, 1)
    pi.set_PWM_dutycycle(STEP, 128)
    print("P-ON")


# Cuts the power to the stepper motors, forcing them to stop.
def stop() -> None:
    pi.set_PWM_dutycycle(STEP, 0)
    pi.write(SLP, 0)
    print("P-OFF")


# Opens the window.
# Note: pi.read(6) reads the upper limit switch.
def open_window() -> None:
    print(pi.read(6))

    # Only run if the window is not already at the top.
    if not(pi.read(6)):
        print("Hello")
        pi.write(DIR, up)
        power_on()

        start_time = time.time()

        # Keep opening until the upper limit switch is hit, then turn off the motors.
        while not(pi.read(6)):
            pass
        stop()

        # Write the time that it took to time.txt.
        end_time = time.time()
        delta_time = end_time - start_time
        with open("./time.txt", "w+") as f:
            f.write(str(delta_time))
        

# Closes the window.
# Note: pi.read(24) reads the lower limit switch.
# Note: The logic here is the same as for open_window(), only with the lower limit switch used instead of the upper limit switch. Refer to comments there for explanations.
def close_window() -> None:
    print(pi.read(24))
    if not(pi.read(24)):
        print("Hello")
        pi.write(DIR, down)
        power_on()

        start_time = time.time()

        while not(pi.read(24)):
            pass
        stop()

        end_time = time.time()
        delta_time = end_time - start_time
        with open("./time.txt", "w+") as f:
            f.write(str(delta_time))