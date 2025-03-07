from functions.touchscreen import touchscreen_watchdog
from functions.receiver import receive_command
from functions.stepper_motor import setup_motors, stop
from functions.distance_sensors import distance_process
from functions.limit_switches import LS_watchdog
from functions.emergency_stop import emergency_stop
from multiprocessing import Process

if __name__ == "__main__":

    stop()

    emergency_stop(False)

    setup_motors()

    remote_process = Process(target=receive_command)

    remote_process.start()

    p_distance = distance_process()

    p_limitSwitches = LS_watchdog()

    # Put this at the end of the file, such that it does not block any other Processes
    p_touchscreen = touchscreen_watchdog()


    remote_process.join()
    p_limitSwitches.join()
    p_distance.join()
    # Join together the processes
    p_touchscreen.join()
    
    print("Done!")

