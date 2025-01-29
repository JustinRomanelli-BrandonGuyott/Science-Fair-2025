from rec2 import check_for_command
import pigpio


SLP = 15

pi = pigpio.pi()

print("on")
pi.write(SLP, 1)

while True:

    while True:
        if check_for_command() == "F Button":
            print("off")
            pi.write(SLP, 0)
        break

    while True:
        if check_for_command() == "Power button":
            print("on")
            pi.write(SLP, 1)
        break


