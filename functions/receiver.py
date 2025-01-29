from functions.power import get_speed, set_speed
from functions.stepper_motor import open_window, close_window, power_on, stop
import evdev


# Get all of the devices. If the RPi is found, then return it
# The name of the IR Receiver is "gpio_ir_recv".
def find_device() -> evdev.device.InputDevice:
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    for device in devices:

        if device.name == "gpio_ir_recv":
            print(f"IR receiver found at path {device.path}\n")
            return device
    print("No objects found.")


# Receives command from the IR receiver.
def receive_command():
    ir_receiver = find_device()

    # The previous event value (event.value).
    # Used to prevent the same button from being pressed multiple times in a row.
    event_old: int = -1 

    while True:
        event = ir_receiver.read_one()

        while not event or not event.value:
            event = ir_receiver.read_one()

        # Prevents the same button from being registered concurrently
        # Exceptions for Power button and F Button (off)
        if (event.value != event_old or (event.value == 460557) or (event.value == 7)):
            event_old = event.value
            print(convert_commands(event.value))
            interpret_command(convert_commands(event.value))


# Interprets the command received from the remote to a function in code.
def interpret_command(command: str) -> None:
    if command == "Volume Up" and get_speed() < 2:
        set_speed(2)

    if command == "Volume Down" and get_speed() > 1:
        set_speed(1)

    if command == "Channel Up":
        open_window()

    if command == "Channel Down":
        close_window()

    if command == "Power Button":
        power_on()

    if command == "F Button":
        stop()

# Converts the integer command value to a human-readable string
def convert_commands(event):
    command_table: dict = {
        0: "No buttons pressed",
        1: None,
        2: "Channel Up",
        3: "Channel Down",
        4: "Volume Down",
        5: "Volume Up",
        6: "Mute",
        7: "F Button",
        460557: "Power Button",
    }

    return command_table.get(event)