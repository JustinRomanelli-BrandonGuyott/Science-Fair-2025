from functions.touchscreen import touchscreen_watchdog
from functions.receiver import receive_command
from functions.stepper_motor import setup_motors
from functions.distance_sensors import distance_watchdog
from multiprocessing import Process

if __name__ == "__main__":

    # Function that stops the motor immediately, in case something goes wrong.
    #stop()

    setup_motors()

    # Set up the IR Remote
    remote_process = Process(target=receive_command)

    remote_process.start()

    # Set up the distance sensor
    # Follows the format: (TRIG, ECHO)
    p_distance = distance_watchdog((13, 16), (19, 20), (26, 21))

    # This is put at the end of the file, such that it does not block any other Processes
    p_touchscreen = touchscreen_watchdog()

    # Join together the processes when finished
    p_touchscreen.join()
    
    remote_process.join()
    
    p_distance.join()
    
    print("Done!")

