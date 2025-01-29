# import pigpio
# import multiprocessing as mp
# from time import sleep, time
# from functions.emergency_stop import emergency_stop
# from functions.stepper_motor import stop

# def limit_switch_watchdog() -> mp.Process:

#     print("WATCHDOG IS RUN")

#     p_limit_switch = mp.Process(target=limit_switch_runner)

#     p_limit_switch.start()

#     return p_limit_switch

# def set_direction(dir):
#     global direction
#     direction = dir
#     print("direction")

# def limit_switch_runner() -> None:
    
#     ls = pigpio.pi()


#     # Set up pins as input/output
#     ls.set_mode(5, pigpio.OUTPUT)
#     ls.set_mode(6, pigpio.INPUT)
#     ls.set_mode(25, pigpio.OUTPUT)
#     ls.set_mode(24, pigpio.INPUT)

#     # Enable Limit Switch Power Pins
#     # 0 means connected, 1 means disconnected
#     ls.write(5, 0)
#     ls.write(25, 0)



#     print("In LS runner")

#     hit_top: bool = False
#     hit_bottom: bool = False

#     while True:

#         # 6 is Top LS, 24 is Bottom LS, 15 is SLP pin on stepper motors
#         if ((ls.read(6) and not hit_top) or (ls.read(24) and not hit_bottom)): # and ls.read(15)):
#             if (ls.read(6)):
#                 hit_top = True
#                 hit_bottom = False
#             elif (ls.read(24)):
#                 hit_top = False
#                 hit_bottom = True
#             print("top: " + str(hit_top))
#             print("bottom: " + str(hit_bottom))
#             print(" ")
#             print("direction")
            

#             if (ls.read(6) and direction == "up"):
#                 stop()
#             if (ls.read(24) and direction == "down"):
#                 stop()
#             print("Limit Switch Hit, Stopping")

#             lines = []

#             with open("./time.txt", "r+") as f:
#                 lines = f.readlines()
#                 f.close()

#             with open("./final_time.txt", "w+") as f:
#                 f.write(str(time() - float(lines[0])))

#                 f.close()
                
