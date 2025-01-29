from functions.stepper_motor import set_frequency

# The current speed.
speed = 2

# Returns the speed variable. Used to help communicate between individual Processes.
def get_speed() -> int:
    global speed
    return speed

# def get_frequency() -> int:
#     with open("./speed.txt", "r") as f:
#         f.seek(0)
#         freq_list = f.readlines()
#         f.close()
#         frequency = int(freq_list[0])
#         return frequency

# Sets the speed to the desired value, as well as setting the frequency of the stepper motors.
def set_speed(s: int) -> None:
    global speed
    speed = s
    if s == 1:
        frequency: int = 800
    elif s == 2:
        frequency: int = 1000

    set_frequency(frequency)

    # with open("./speed.txt", "w+") as f:
    #     f.write(str(frequency))
    #     f.close()
    
    # status_list: list[str, str, str] = [] 

    # with open("./status.txt", "r") as f:
    #     status_list: list[str, str] = f.readlines()

    #     f.close()

    # with open("./status.txt", "w+") as f:
    #     # list[0] is the speed, list[1] is the status
    
    #     f.seek(0)


    #     # Get the part after the "Status:"
    #     # if status_list[1].split(" ")[1][0].lower() == "o":
    #     #     f.write(f"{s}\n{s}\n{status_list[2]}")
    #     # elif status_list[1].split(" ")[1][0].lower() == "c":
    #     #     f.write(f"{s}\n{s}\n{status_list[2]}")
    #     # elif status_list[1].split(" ")[1].lower() == "paused":
    #     #     f.write(f"{s}\n{s}\n{status_list[2]}")
    #     # elif status_list[1].split(" ")[1].lower() == "resumed":
    #     #     f.write(f"{s}\n{s}\n{status_list[2]}")

    #     f.close()


# def status_set(status: str) -> None:
    
#     status_list: list[str, str, str] = [] 

#     with open("./status.txt", "r") as f:
#         status_list = f.readlines()

#         f.close()

#     with open("./status.txt", "w+") as f:
#         # list[0] is the speed, list[1] is the status, list[2] is the time
    
#         f.seek(0)

#         f.write(f"{status_list[0]}")
#         f.write(f"{status_list[1]}")
#         f.write(f"{status_list[2]}")

#         f.close()

# Writes the time that the motor took to open to a file named status.txt in the root directory.
# Used to communicate between Processes.
def time_set(time: float) -> None:

    status_list: list[str, str, str] = [] 

    with open("./status.txt", "r") as f:
        status_list = f.readlines()

        f.close()

    with open("./status.txt", "w+") as f:
        # list[0] is the speed, list[1] is the status
    
        f.seek(0)

        f.write(f"{status_list[0]}{status_list[1]}{str(time)}")
