import multiprocessing as mp
import pigpio
import time
from functions.emergency_stop import emergency_stop, led_resume

# NOTE: All "pins" objects are formatted such that pins[0] = TRIG and pins[1] = ECHO

# Establishes the distance sensor's connection to the Pi.
pi_ds = pigpio.pi()

# Setup function for the distance.
# Starts the process but does not run Process.join() until the end of main.py.
# TODO: UPDATE PIN VALUES
def distance_watchdog(
    pins1: tuple[int, int], pins2: tuple[int, int], pins3: tuple[int, int]
    ) -> mp.Process:
    # NOTE: PIN VALUES:
    # pins1 = (13, 16)
    # pins2 = (19, 20)
    # pins3 = (26, 21)

    #print("Distance measurement tare 1 in process")

    #window_length_1: float = initialize_variables(pins1)

    #print("Distance measurement tare 2 in process")

    #window_length_2: float = initialize_variables(pins2)

    print("Distance measurement tare 3 in process")

    # Creates the average window length for the third distance sensor.
    # Also initializes the TRIG and ECHO pins.
    window_length_3: float = initialize_variables(pins3)

    # Create and run the Process.

    #p1 = mp.Process(target=analyze_distance, args=(pins1, window_length_1))
    #p2 = mp.Process(target=analyze_distance, args=(pins2, window_length_2))
    p3 = mp.Process(target=analyze_distance, args=(pins3, window_length_3))

    #p1.start()
    #time.sleep(1.2)
    #p2.start()
    p3.start()

    # Return the Process such that join() can be runned at the end of main.py.
    return p3

# Initializes the variables to set up each distance sensor.
# Also creates an average value for the length of the window.
def initialize_variables(pins: tuple[int, int]) -> float:

    # Setup
    TRIG: int = pins[0]
    ECHO: int = pins[1]

    pi_ds.set_mode(TRIG, pigpio.OUTPUT)
    pi_ds.set_mode(ECHO, pigpio.INPUT)

    pi_ds.write(TRIG, 0)
    print("Waiting for sensor...")

    time.sleep(2)

    tare_sum: float = 0

    # Find the distance of the window five times, then take the average distance and return it.

    for i in range(5):
        setup_distance = round(get_distance(pins), 2)
        tare_sum += setup_distance
        time.sleep(0.5)

    window_length = round(tare_sum / 5, 2)

    return window_length

# Gets the distance from the distance sensor itself.
def get_distance(pins: tuple[int, int]) -> float:
    TRIG: int = pins[0]
    ECHO: int = pins[1]

    count = 0

    pi_ds.write(TRIG, 1)
    time.sleep(0.25)
    pi_ds.write(TRIG, 0)

    # Note: This will break out of the loop if it takes too long.
    # We hypothesize that this occurs when one of the distance sensors sends out a signal, but does not get it back (either due to interference with other distance sensors or with the object itself).
    while pi_ds.read(ECHO) == 0:
        count += 1
        if (count > 20000):
            print("TOOK TOO LONG, BREAKING OUT OF LOOP")
            # A value of -1.0 indicates an error.
            return -1.0

    count = 0
    
    # Time of when the pulse starts.
    pulse_start = time.time()
    
    # See the comment above the while loop for the reasoning behind the break condition.
    while pi_ds.read(ECHO) == 1:
        count += 1
        if (count > 20000):
            print("TOOK TOO LONG, BREAKING OUT OF LOOP")
            return -1.0
    
    # Get the total time it took
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Find the distance from the time it took.
    distance = pulse_duration * 17150

    distance = round(distance, 2)

    #print("Distance: " + str(distance) + " cm, TRIG = " + str(TRIG))

    return distance

# Analyze the distance, and run emergency_stop() if an object is detected.
def analyze_distance(pins: tuple[int, int], window_length: float = -1.0) -> None:
    if window_length < 0:
        raise Exception("Window Length was set to a negative number or was not set!")

    #TRIG: int = pins[0]
    #ECHO: int = pins[1]

    # This is run by a Process, so the while True will run until the process is closed.

    # The logic is as follows:
    # Check to see if the distance is less than the window length minus 12.
    # Or, if the distance is greater than the window length plus 12 (indicating an error with the measurement, as there should not be a value greater than the window length).
    # If True, then run the function again with the same condition to see if the first measurement was accurate.
    # If True, then run emergency_stop() from emergency_stop.py.

    # Note: If the distance sensor does not detect an object (emergency_stop() is not run), then the green LED is turned on and the other LEDs are turned off.

    while True:
        distance = get_distance(pins)
        #print(distance)
        if (distance < (window_length - 12) or distance > (window_length + 12)):
            time.sleep(0.005)
            distance = get_distance(pins)
            if (distance < (window_length - 12) or distance > (window_length + 12)):
                if distance > 0:
                    emergency_stop(True)
                    print("Emergency Stop")
        else:
            led_resume()