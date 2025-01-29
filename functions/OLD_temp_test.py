import time
from power import time_set

def read_write() -> None:
    start_time = time.time()

    input()

    end_time = time.time()

    print("Setting time")
    time_set(end_time - start_time)