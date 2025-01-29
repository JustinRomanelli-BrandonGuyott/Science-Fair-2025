from functions.LED_functions import red_led_off, green_led_off, green_led_on, yellow_led_off, yellow_led_on
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from functions.stepper_motor import open_window
import multiprocessing as mp
import os
import time
import schedule

# TODO: CHANGE IMAGE FILE DIRECTORIES ONCE TESTING IS DONE WITH TOUCHSCREEN
# TODO: Figure out what's going on with the speed buttons, and how to change the speed on the open/close functions.

speed: int = 1

# Final functions are below
def touchscreen_watchdog() -> None:
    p_touchscreen = mp.Process(target=tkinter_runner)

    p_touchscreen.start()

    # TODO: TEMP
    open_window()

    p_touchscreen.join()

    print("Exiting touchscreen...")


def tkinter_runner() -> None:
    # General
    global string_status

    # Main page
    global label_status
    global label_motion
    global label_speed
    global label_operation

    global panel_up_arrow
    global panel_down_arrow
    global panel_plus_sign
    global panel_minus_sign
    global panel_pause
    global panel_resume
    global panel_stats

    global label_title_bar
    global label_status_bar

    # Statistics page
    global string_timer

    global label_timer

    global panel_x

    #p_checker = mp.Process(target=update_status)

    #p_checker.start()


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

    # Statistics Button, opens up the statistics page

    image_temp = Image.open("../imgs/statistics_clipart.png")
    resized_image_temp = image_temp.resize((int(75 * 1.875), int(75 * 1.8)))
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
    )
    panel_stats.place(relx=0.04, rely=0.85, anchor=CENTER)

    # Title / Status Bars

    img_temp = Image.open("../imgs/title_bar.png")
    resized_image_temp = img_temp.resize((3000, int(50 * 1.8)))

    img_title_bar = ImageTk.PhotoImage(resized_image_temp)
    label_title_bar = Label(root, image=img_title_bar, height=50 * 1.8)
    label_title_bar.place(x=-100 * 1.875, y=0)

    img_temp = Image.open("../imgs/status_bar.png")
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
    string_speed.set("Speed")
    label_speed = Label(
        root,
        textvariable=string_speed,
        font=("Arial", 40, "bold"),
        bg="#4782b5",
        fg="white",
    )
    label_speed.place(anchor=CENTER, relx=0.49, rely=0.04)

    string_operation = StringVar()
    string_operation.set("Operation")
    label_operation = Label(
        root,
        textvariable=string_operation,
        font=("Arial", 40, "bold"),
        bg="#4782b5",
        fg="white",
    )
    label_operation.place(anchor=CENTER, relx=0.775, rely=0.04)

    # Status Label

    string_status = StringVar()
    string_status.set("Status: None")
    label_status = Label(
        root,
        textvariable=string_status,
        font=("Arial", 44, "bold"),
        bg="#992424",
        fg="white",
    )
    label_status.place(x=10 * 1.875, y=556 * 1.8)

    # Motion Buttons

    image_temp = Image.open("../imgs/up_arrow.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.8)))
    img_up_arrow = ImageTk.PhotoImage(resized_image_temp)

    panel_up_arrow = Button(
        mainframe,
        image=img_up_arrow,
        command=root.quit,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_up_arrow.grid(column=0, row=1, padx=(110 * 1.875, 0), pady=(90 * 1.8, 30 * 1.8))

    image_temp = Image.open("../imgs/down_arrow.png")
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

    # Speed Buttons

    image_temp = Image.open("../imgs/plus_sign.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.8)))
    img_plus_sign = ImageTk.PhotoImage(resized_image_temp)

    panel_plus_sign = Button(
        mainframe,
        image=img_plus_sign,
        command=speed_up,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_plus_sign.grid(column=1, row=1, padx=(int(110 * 1.875), int(110 * 1.875)), pady=(90 * 1.8, 30 * 1.8))

    image_temp = Image.open("../imgs/minus_sign.png")
    resized_image_temp = image_temp.resize((int(180 * 1.875), int(180 * 1.875)))
    img_minus_sign = ImageTk.PhotoImage(resized_image_temp)

    panel_minus_sign = Button(
        mainframe,
        image=img_minus_sign,
        command=slow_down,
        borderwidth=0,
        background=BKG_COLOR,
        activebackground=BKG_COLOR,
        activeforeground=BKG_COLOR,
        relief=SUNKEN,
        width=180 * 1.875,
        height=180 * 1.8,
    )
    panel_minus_sign.grid(column=1, row=2, padx=(int(110 * 1.875), int(110 * 1.875)), pady=(30 * 1.8, 90 * 1.8))

    # Pause / Play Buttons

    image_temp = Image.open("../imgs/pause_sign.png")
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
    panel_pause.grid(column=2, row=1, padx=(0, int(110 * 1.875)), pady=(90 * 1.8, 30 * 1.8))

    image_temp = Image.open("../imgs/resume_sign.png")
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
    panel_resume.grid(column=2, row=2, padx=(0, int(110 * 1.875)), pady=(30 * 1.8, 90 * 1.8))

    # X Button (Statistics Page)

    img_temp = Image.open("../imgs/x_clipart.png")
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


def show_main() -> None:
    panel_up_arrow.grid(column=0, row=1, padx=(int(110 * 1.875), 0), pady=(90 * 1.8, 30 * 1.8))
    panel_down_arrow.grid(column=0, row=2, padx=(int(110 * 1.875), 0), pady=(30 * 1.8, 90 * 1.8))
    panel_plus_sign.grid(column=1, row=1, padx=(int(110 * 1.875), int(110 * 1.875)), pady=(90 * 1.8, 30 * 1.8))
    panel_minus_sign.grid(column=1, row=2, padx=(int(110 * 1.875), int(110 * 1.875)), pady=(30 * 1.8, 90 * 1.8))
    panel_pause.grid(column=2, row=1, padx=(0, int(110 * 1.875)), pady=(90 * 1.8, 30 * 1.8))
    panel_resume.grid(column=2, row=2, padx=(0, int(110 * 1.875)), pady=(30 * 1.8, 90 * 1.8))

    panel_stats.place(x=0, y=0, relx=0.04, rely=0.85, anchor=CENTER)

    label_title_bar.place(x=-100 * 1.875, y=0, relx=0, rely=0)
    label_status_bar.place(x=-200 * 1.875, y=550 * 1.8, relx=0, rely=0)
    label_status.place(x=5 * 1.875, y=556 * 1.8, relx=0, rely=0)
    label_motion.place(anchor=CENTER, relx=0.2, rely=0.04)
    label_speed.place(anchor=CENTER, relx=0.49, rely=0.04)
    label_operation.place(anchor=CENTER, relx=0.775, rely=0.04)


def show_stats() -> None:
    panel_x.place(x=0, y=0, relx=0.025, rely=0.025)
    label_timer.place(x=0, y=0, relx=0.5, rely=0.5, anchor=CENTER)

    # TODO: THIS IS TEMPORARY. REMOVE IT WHEN DONE TESTING
    #time_window()


def hide_main() -> None:
    # Leave this commented for the duration of testing the function.
    # Uncomment when a way to break out of the function has been made (exiting the stats page)
    panel_up_arrow.grid_forget()
    panel_down_arrow.grid_forget()
    panel_plus_sign.grid_forget()
    panel_minus_sign.grid_forget()
    panel_pause.grid_forget()
    panel_resume.grid_forget()

    panel_stats.place(x=-200 * 1.875, y=-200 * 1.8, relx=0, rely=0)

    label_title_bar.place(relx=1.5, rely=1.5)
    label_status_bar.place(relx=1.5, rely=1.5)
    label_status.place(relx=1.5, rely=1.5)
    label_motion.place(relx=1.5, rely=1.5)
    label_speed.place(relx=1.5, rely=1.5)
    label_operation.place(relx=1.5, rely=1.5)


def hide_stats() -> None:
    panel_x.place(x=-200 * 1.875, y=-200 * 1.8, relx=0, rely=0)
    label_timer.place(x=-200 * 1.875, y=-200 * 1.8, relx=0, rely=0)


# TODO: Make a stats page quickly that just has calculated time.
# Use hide_main() and show_main(), along with some kind of X button, to exit out
def open_stats_page() -> None:
    hide_main()
    show_stats()


def close_stats_page() -> None:
    hide_stats()
    show_main()


def start_timer() -> float:
    return time.time()


def end_timer() -> float:
    return time.time()


def time_window() -> None:
    start_time: float = start_timer()
    end_time: float = end_timer()
    final_time: float = end_time - start_time

    while final_time < 10:
        end_time = end_timer()
        final_time = end_time - start_time
        string_timer.set(f"Calculated Time: {final_time:.3f} seconds")
        label_timer.update()

    print(f"Time elapsed: {end_time - start_time} seconds")
    print(
        f"  {end_time}\n- {start_time}\n------------------\n= {end_time - start_time}"
    )
    string_timer.set(
        "Calculated Time: " + str(round(end_time - start_time, 2)) + " seconds"
    )


# The functions below are all temporary and are for testing.


def raise_window(speed: int) -> None:
    print("raise_window")
    string_status.set("Status: Opening window with Speed " + str(speed) + "...")


def lower_window() -> None:
    print("lower_window")
    string_status.set("Status: Closing window with a Speed (CHANGE LATER)")#  + str(speed) + "...")

    red_led_off()
    yellow_led_off()
    green_led_on()

    time_window()

    # Testing; open stats page when button is pressed.
    # open_stats_page()


def speed_up() -> None:
    print("speed_up")
    # panel_up_arrow.configure()
    panel_down_arrow.configure(command=lower_window())
    speed = 2


def slow_down() -> None:
    print("slow_down")
    # panel_up_arrow.configure()
    panel_down_arrow.configure(command=lower_window())
    speed = 1


def pause() -> None:
    print("pausing")
    
    red_led_off()
    yellow_led_on()
    green_led_off()

    string_status.set("Status: Paused")


def resume() -> None:
    print("resuming")
    red_led_off()
    yellow_led_off()
    green_led_on()
    string_status.set("Status: Resumed")

# def update_status() -> None:
    
#     with open("../status.txt", "r") as f:

#         status_list: list[str, str, str] = f.readlines() 

#         for status in status_list:
#             print(status)

#         string_status.set(status_list[1])
#         string_timer.set(status_list[2])

#         f.close()
#     label_status.update()
#     label_timer.update()


if __name__ == "__main__":
    touchscreen_watchdog()
