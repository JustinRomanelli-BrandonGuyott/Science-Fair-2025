import multiprocessing as mp
import RPi.GPIO as GPIO
import time
#from emergency_stop import emergency_stop

# NOTE: All "pins" objects are formatted such that pins[0] = TRIG and pins[1] = ECHO


# TODO: UPDATE PIN VALUES
def distance_watchdog(
    pins1: tuple[int, int], pins2: tuple[int, int], pins3: tuple[int, int]
    ) -> None:
    # NOTE: PIN VALUES:
    # pins1 = (13, 16)
    # pins2 = (19, 20)
    # pins3 = (26, 21)

    print("Distance measurement 1 in process")

    window_length_1: float = initialize_variables(pins1)

    #print("Distance measurement 2 in process")

    #window_length_2: float = initialize_variables(pins2)

    #print("Distance measurement 3 in process")

    #window_length_3: float = initialize_variables(pins3)

    p1 = mp.Process(target=analyze_distance, args=(pins1, window_length_1))
    #p2 = mp.Process(target=analyze_distance, args=(pins2, window_length_2))
    #p3 = mp.Process(target=analyze_distance, args=(pins3, window_length_3))

    p1.start()
    #p2.start()
    #p3.start()

    p1.join()
    #p2.join()
    #p3.join()

    print("Done!")


def initialize_variables(pins: tuple[int, int]) -> float:
    GPIO.setmode(GPIO.BCM)

    TRIG: int = pins[0]
    ECHO: int = pins[1]

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    print("Waiting for sensor...")

    time.sleep(2)

    tare_sum: float = 0

    for i in range(5):
        setup_distance = round(get_distance(pins), 2)
        tare_sum += setup_distance
        time.sleep(0.5)

    window_length = round(tare_sum / 5, 2)

    return window_length


def get_distance(pins: tuple[int, int]) -> float:
    TRIG: int = pins[0]
    ECHO: int = pins[1]

    GPIO.output(TRIG, True)

    time.sleep(0.00001)

    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print("Distance: " + str(distance) + " cm, TRIG = " + str(TRIG))

    GPIO.cleanup()
    time.sleep(2)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    return distance


def analyze_distance(pins: tuple[int, int], window_length: float = -1.0) -> None:
    if window_length < 0:
        raise Exception("Window Length was set to a negative number or was not set!")

    #TRIG: int = pins[0]
    #ECHO: int = pins[1]

    try:
        while True:
            distance = get_distance(pins)
            if (distance < (window_length-8)) or (distance > (window_length+8)):
                #emergency_stop()
                print("Emergency Stop")
            else:
                print(str(distance))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()

    return



distance_watchdog((13, 16), (19, 20), (26, 21))