from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from functions.LED_functions import red_led_off, green_led_off, green_led_on, yellow_led_off, yellow_led_on
from functions.stepper_motor import open_window, close_window, power_on, stop
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import multiprocessing as mp
import os
import time

# This speed variable is not used to great capacity.
speed: int = 1

# Update the time (for statistics page). The TextUpdateHandler is not used to do anything, although it does exist.

class TextUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == "/home/brandon/Science_Fair_2025/status.txt":
            update_status(True)


class TimeUpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == "/home/brandon/Science_Fair_2025/final_time.txt":
            update_status(False)

# Final functions are below


def touchscreen_watchdog() -> mp.Process:
    p_touchscreen = mp.Process(target=tkinter_runner)

    p_touchscreen.start()

    return p_touchscreen

def tkinter_runner() -> None:
    # General
    global speed
    global down_arrow_active

    # Main page
    global label_motion
    global label_speed
    global label_operation

    global panel_up_arrow
    global panel_down_arrow
    global panel_pause
    global panel_resume
    global panel_stats
    global panel_settings

    global label_title_bar
    global label_status_bar

    # Statistics page
    global string_timer

    global label_timer

    global panel_x

    down_arrow_active = False

    observer = Observer()

    path = os.path.abspath(".")
    event_handler = TextUpdateHandler()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    observer_1 = Observer()
    event_handler_1 = TimeUpdateHandler()
    observer_1.schedule(event_handler_1, path, recursive=False)
    observer_1.start()

    # Set the display to the touchscreen
    if os.environ.get("DISPLAY", "") == "":
        print("No Display Found, Using :0.0")
        os.environ.__setitem__("DISPLAY", ":0.0")

    BKG_COLOR = "#d9d9d9"

    # Configure root and mainframe

    root = Tk()
    root.title("Science Fair 2025 Application")
    root.configure(background=BKG_COLOR)

    # Switch these according to whether this is being tested on the Touchscreen or not.
    root.attributes('-fullscreen', True)
    #root.geometry("1024x768")

    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0, sticky=N + S + E + W)

    # Title / Status Bars

    img_temp = Image.open("./imgs/title_bar.png")
    resized_image_temp = img_temp.resize((3000, int(50 * 1.8)))

    img_title_bar = ImageTk.PhotoImage(resized_image_temp)
    label_title_bar = Label(root, image=img_title_bar, height=50 * 1.8)
    label_title_bar.place(x=-100 * 1.875, y=0)

    img_temp = Image.open("./imgs/status_bar.png")
    resized_image_temp = img_temp.resize((3000, int(50 * 1.8)))

    img_status_bar = ImageTk.PhotoImage(resized_image_temp)
    label_status_bar = Label(root, image=img_status_bar, height=50 * 1.8)
    label_status_bar.place(x=-100 * 1.875, y=550 * 1.8)

    # Title Labels
    # TODO: Make these positions exact, not just approximate.
    #  As of right now, the values for relx of each label is arbitrary.

    string_motion = StringVar()
    string_motion.set("Motion")
    label_motion = Label(
        root,
        textvariable=string_motion,
        font=("Arial", 40, "bold"),
        bg="#4782b5",
        fg="white",
    )
    label_motion.place(anchor=CENTER, relx=0.2, rely=0.04)

    string_speed = StringVar()
    string_speed.set("Operation")
    label_speed = Label(
        root,
        textvariable=string_speed,
        font=("Arial", 40, "bold"),
        bg="#4782b5",
        fg="white",
    )
    label_speed.place(anchor=CENTER, relx=0.49, rely=0.04)

    string_operation = StringVar()
    string_operation.set("Settings")
    label_operation = Label(
        root,
        textvariable=string_operation,
        font=("Arial", 40, "bold"),
        bg="#4782b5",
        fg="white",
    )
    label_operation.place(anchor=CENTER, relx=0.775, rely=0.04)

    # Motion Buttons

    image_temp = Image.open("./imgs/up_arrow.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.8)))
    img_up_arrow = ImageTk.PhotoImage(resized_image_temp)

    panel_up_arrow = Button(
        mainframe,
        image=img_up_arrow,
        command=raise_window,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_up_arrow.grid(column=0, row=1, padx=(110 * 1.875, 0), pady=(90 * 1.8, 30 * 1.8))

    image_temp = Image.open("./imgs/down_arrow.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.8)))
    img_down_arrow = ImageTk.PhotoImage(resized_image_temp)

    panel_down_arrow = Button(
        mainframe,
        image=img_down_arrow,
        command=lower_window,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_down_arrow.grid(column=0, row=2, padx=(int(110 * 1.875), 0), pady=(30 * 1.8, 90 * 1.8))

    # Pause / Play Buttons

    image_temp = Image.open("./imgs/pause_sign.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.8)))
    img_pause = ImageTk.PhotoImage(resized_image_temp)

    panel_pause = Button(
        mainframe,
        image=img_pause,
        command=pause,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_pause.grid(column=1, row=1, padx=(int(110 * 1.875), int(110 * 1.875)), pady=(90 * 1.8, 30 * 1.8))

    image_temp = Image.open("./imgs/resume_sign.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.8)))
    img_resume = ImageTk.PhotoImage(resized_image_temp)

    panel_resume = Button(
        mainframe,
        image=img_resume,
        command=resume,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_resume.grid(column=1, row=2, padx=(int(110 * 1.875), int(110 * 1.875)), pady=(30 * 1.8, 90 * 1.8))

    # Settings Buttons
    
    image_temp = Image.open("./imgs/statistics_sign.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.8)))
    img_stats = ImageTk.PhotoImage(resized_image_temp)

    panel_stats = Button(
        mainframe,
        image=img_stats,
        command=open_stats_page,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_stats.grid(column=2, row=1, padx=(0, int(110 * 1.875)), pady=(90 * 1.8, 30 * 1.8))
    
    image_temp = Image.open("./imgs/gear_sign.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.8)))
    img_settings = ImageTk.PhotoImage(resized_image_temp)

    panel_settings = Button(
        mainframe,
        image=img_settings,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_settings.grid(column=2, row=2, padx=(0, int(110 * 1.875)), pady=(30 * 1.8, 90 * 1.8))

    # X Button (Statistics Page)

    img_temp = Image.open("./imgs/x_clipart.png")
    resized_image_temp = img_temp.resize((int(48 * 1.875), int(48 * 1.8)))
    img_x = ImageTk.PhotoImage(resized_image_temp)

    panel_x = Button(
        mainframe,
        image=img_x,
        command=close_stats_page,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
    )
    panel_x.place(relx=1.5, rely=1.5)

    # Timer Label (Statistics Page)

    string_timer = StringVar()
    string_timer.set("Calculated Time: N/A")
    label_timer = Label(
        root, textvariable=string_timer, font=("Arial", 50), bg=BKG_COLOR, fg="Black"
    )
    label_timer.place(x=-200 * 1.875, y=-200 * 1.8)

    # Run the main loop.
    root.mainloop()


# Functions to update the touchscreen's display: from main to statistics or vice versa.

def show_main() -> None:
    panel_up_arrow.grid(column=0, row=1, padx=(int(110 * 1.875), 0), pady=(90 * 1.8, 30 * 1.8))
    panel_down_arrow.grid(column=0, row=2, padx=(int(110 * 1.875), 0), pady=(30 * 1.8, 90 * 1.8))
    panel_pause.grid(column=1, row=1, padx=(int(110 * 1.875), int(110 * 1.875)), pady=(90 * 1.8, 30 * 1.8))
    panel_resume.grid(column=1, row=2, padx=(int(110 * 1.875), int(110 * 1.875)), pady=(30 * 1.8, 90 * 1.8))
    panel_stats.grid(column=2, row=1, padx=(0, int(110 * 1.875)), pady=(90 * 1.8, 30 * 1.8))
    panel_settings.grid(column=2, row=2, padx=(0, int(110 * 1.875)), pady=(30 * 1.8, 90 * 1.8))

    label_title_bar.place(x=-100 * 1.875, y=0, relx=0, rely=0)
    label_status_bar.place(x=-200 * 1.875, y=550 * 1.8, relx=0, rely=0)
    label_motion.place(anchor=CENTER, relx=0.2, rely=0.04)
    label_speed.place(anchor=CENTER, relx=0.49, rely=0.04)
    label_operation.place(anchor=CENTER, relx=0.775, rely=0.04)


def show_stats() -> None:
    panel_x.place(x=0, y=0, relx=0.025, rely=0.025)
    label_timer.place(x=0, y=0, relx=0.5, rely=0.5, anchor=CENTER)


def hide_main() -> None:
    panel_up_arrow.grid_forget()
    panel_down_arrow.grid_forget()
    panel_pause.grid_forget()
    panel_resume.grid_forget()
    panel_stats.grid_forget()
    panel_settings.grid_forget()

    label_title_bar.place(relx=1.5, rely=1.5)
    label_status_bar.place(relx=1.5, rely=1.5)
    label_status.place(relx=1.5, rely=1.5)
    label_motion.place(relx=1.5, rely=1.5)
    label_speed.place(relx=1.5, rely=1.5)
    label_operation.place(relx=1.5, rely=1.5)


def hide_stats() -> None:
    panel_x.place(x=-200 * 1.875, y=-200 * 1.8, relx=0, rely=0)
    label_timer.place(x=-200 * 1.875, y=-200 * 1.8, relx=0, rely=0)


def open_stats_page() -> None:
    hide_main()
    show_stats()


def close_stats_page() -> None:
    hide_stats()
    show_main()


# These functions are used when one of the buttons that affects the window is pressed (all but statistics and settings)

def raise_window() -> None:

    open_window()


def lower_window() -> None:

    close_window()


def pause() -> None:
    print("PAUSED")
    stop()


def resume() -> None:
    print("RESUMING")
    power_on()

# The "is_status" part of this code is not used.
def update_status(is_status: bool) -> None:

    global speed
    global string_timer

    status_list: list[str]

    if is_status:
        with open("./status.txt", "r") as f:
            f.seek(0)
            status_list = f.readlines()
            f.close()

        if status_list:
            
            speed = int(status_list[0][0])

            #string_status.set(status_list[1])
            #string_timer.set(f"Calculated Time: " + str(round(float(status_list[2]), 3)))

            #label_status.update()
            #label_timer.update()
        else:
            print("The file is empty or does not contain any lines.")

    else:
        with open("./final_time.txt", "r") as f:
            f.seek(0)
            status_list = f.readlines()
            f.close()
        
        if status_list and float(status_list[0]) < 1000000:
            string_timer.set(f"Calculated Time: {str(round(float(status_list[0]), 4))}")

            label_timer.update()
