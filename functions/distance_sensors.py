import RPi.GPIO as GPIO
from time import sleep, time
from functions.emergency_stop import emergency_stop
from multiprocessing import Process

# *** FUNCTIONS ***
def write_is_safe(safeToClose):
    with open("./safe_to_close.txt", "r") as f:
        status = f.read()
        f.close()
        
        if not(status == str(safeToClose)):
            with open("./safe_to_close.txt", "w+") as f:
                f.write(str(safeToClose))
                f.close()

def initialize_distance(trigpin, echopin):

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigpin, GPIO.OUT)
    GPIO.setup(echopin, GPIO.IN)

def get_distance(trigpin, echopin):
    count = 0
    
    GPIO.output(trigpin, True)
    sleep(0.03)
    GPIO.output(trigpin, False)
    while GPIO.input(echopin) == 0:
        count += 1
        if (count > 200000):
            print("TOOK TOO LONG, BREAKING OUT OF LOOP; TRIGPIN: " + str(trigpin) + " ECHOPIN: "  + str(echopin))
            return -1.0

    echoStartTime = time()
    while GPIO.input(echopin) == 1:
        count += 1
        if (count > 200000):
            print("TOOK TOO LONG, BREAKING OUT OF LOOP; TRIGPIN: " + str(trigpin) + " ECHOPIN: " + str(echopin))
            return -1.0
    echoEndTime = time()

    echoTime = echoEndTime - echoStartTime
    calculated_distance = round(echoTime * 17150, 2)

    return calculated_distance

# Returns True if there is an object detected in the window, else returns False
def analyze_distance(trig, echo, window_length):
    sleep(0.025) # KEEP THIS IN FOR NOW, CONSISTENCY
    distance = round(get_distance(trig, echo), 2)

    if (((distance < (window_length - 8)) or (distance > (window_length + 8))) and distance > 0):
        # These lines prevent random measurements from triggering emergency stop, but it also makes it slower. Comment out if needed.
        sleep(0.025)
        distance = round(get_distance(trig, echo), 2)
        if (((distance < (window_length - 8)) or (distance > (window_length + 8))) and distance > 0):
            return True

    return False

def distance_process():
    p_ds = Process(target=distance_watchdog)
    p_ds.start()
    return p_ds


def distance_watchdog():
    # Bottom DS
    b_trigpin = 26
    b_echopin = 21

    # Middle DS
    m_trigpin = 19
    m_echopin = 20

    # Top DS
    t_trigpin = 13
    t_echopin = 16

    tare_sum = 0

    initialize_distance(b_trigpin, b_echopin)
    initialize_distance(m_trigpin, m_echopin)
    initialize_distance(t_trigpin, t_echopin)

    print("Setting up distance sensors...")

    i = 0

    while (i < 10):
        setup_distance = round(get_distance(b_trigpin, b_echopin), 2)
        print(setup_distance)

        if setup_distance < 30 and setup_distance > 20:
            tare_sum += setup_distance
            i += 1
        sleep(0.5)

    b_window_length = round(tare_sum/10, 2)

    print("Bottom sensor window length: " + str(b_window_length))

    i = 0
    tare_sum = 0

    while (i < 10):
        setup_distance = round(get_distance(m_trigpin, m_echopin), 2)
        print(setup_distance)

        if setup_distance < 30 and setup_distance > 20:
            tare_sum += setup_distance
            i += 1
        sleep(0.5)

    m_window_length = round(tare_sum/10, 2)

    print("Middle sensor window length: " + str(m_window_length))

    i = 0
    tare_sum = 0

    while (i < 10):
        setup_distance = round(get_distance(t_trigpin, t_echopin), 2)
        print(setup_distance)

        if setup_distance < 30 and setup_distance > 20:
            tare_sum += setup_distance
            i += 1
        sleep(0.5)

    t_window_length = round(tare_sum/10, 2)

    print("Top sensor window length: " + str(t_window_length))

    tare_sum = 0

    print("Distance sensors are ready!")

    sleep(2.5)

    b_state = False

    m_state = False

    t_state = False

    while True:
        b_state = analyze_distance(b_trigpin, b_echopin, b_window_length)

        m_state = analyze_distance(m_trigpin, m_echopin, m_window_length)

        t_state = analyze_distance(t_trigpin, t_echopin, t_window_length)
        
        if (b_state or m_state or t_state):
        
            if (b_state):
                distance = round(get_distance(b_trigpin, b_echopin), 2)
                
                while (distance < (b_window_length - 8)) or (distance > (b_window_length + 8)):
                    if (distance > 0):
                        emergency_stop(True)
                        #retract()
                        write_is_safe(False)

                    distance = round(get_distance(b_trigpin, b_echopin), 2)
                    #print(f"Emergency Distance: {distance}\nWindow Length: {b_window_length}")
                    distance = float(distance)
                    sleep(0.025)

                emergency_stop(False)
                write_is_safe(True)
            
            elif (m_state):
                distance = round(get_distance(m_trigpin, m_echopin), 2)
                
                while (distance < (m_window_length - 8)) or (distance > (m_window_length + 8)):
                    if (distance > 0):
                        emergency_stop(True)
                        #retract()
                        write_is_safe(False)

                    distance = round(get_distance(m_trigpin, m_echopin), 2)
                    #print(f"Emergency Distance: {distance}\nWindow Length: {m_window_length}")
                    distance = float(distance)
                    sleep(0.025)

                emergency_stop(False)
                write_is_safe(True)
            
            elif (t_state):
                distance = round(get_distance(t_trigpin, t_echopin), 2)
                
                while (distance < (t_window_length - 8)) or (distance > (t_window_length + 8)):
                    if (distance > 0):
                        emergency_stop(True)
                        #retract()
                        write_is_safe(False)

                    distance = round(get_distance(t_trigpin, t_echopin), 2)
                    #print(f"Emergency Distance: {distance}\nWindow Length: {t_window_length}")
                    distance = float(distance)
                    sleep(0.025)

                emergency_stop(False)
                write_is_safe(True)
