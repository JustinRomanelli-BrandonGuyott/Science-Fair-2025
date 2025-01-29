#from functions.stepper_motor import set_frequency

speed = 2

def get_speed() -> int:
    global speed
    return speed

def set_speed(s: int) -> None:
    global speed
    speed = s

    if s == 1:
        frequency: int = 800
    elif s == 2:
        frequency: int = 1000
    
    status_list: list[str, str, str] = [] 

    with open("../status.txt", "r") as f:
        status_list: list[str, str] = f.readlines()

        f.close()

    with open("../status.txt", "w+") as f:
        # list[0] is the speed, list[1] is the status
    
        f.seek(0)

        # Get the part after the "Status:"
        if status_list[1].split(" ")[1][0].lower() == "o":
            f.write(f"{s}\nStatus: Opening window with Speed {s}\n{status_list[2]}")
        elif status_list[1].split(" ")[1][0].lower() == "c":
            f.write(f"{s}\nStatus: Closing window with Speed {s}\n{status_list[2]}")
        elif status_list[1].split(" ")[1].lower() == "paused":
            f.write(f"{s}\n{status_list[1]}\n{status_list[2]}")
        elif status_list[1].split(" ")[1].lower() == "resumed":
            f.write(f"{s}\n{status_list[1]}\n{status_list[2]}")

        f.close()
        

    #set_frequency(frequency)

def status_set(status: str) -> None:
    
    status_list: list[str, str, str] = [] 

    with open("../status.txt", "r") as f:
        status_list = f.readlines()

        for status in status_list:
            print(status)

        f.close()

    with open("../status.txt", "w+") as f:
        # list[0] is the speed, list[1] is the status, list[2] is the time
    
        f.seek(0)

        f.write(f"{status_list[0]}{status_list[1]}{status_list[2]}")

        f.close()


def time_set(time: float) -> None:

    status_list: list[str, str, str] = [] 

    with open("./status.txt", "r") as f:
        status_list = f.readlines()

        f.close()

    with open("./status.txt", "w+") as f:
        # list[0] is the speed, list[1] is the status
    
        f.seek(0)

        f.write(f"{status_list[0]}{status_list[1]}{str(time)}")
