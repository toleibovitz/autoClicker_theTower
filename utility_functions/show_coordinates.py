import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()  # get the current mouse position
        print(f"Mouse position: X={x}, Y={y}", end='\r')  # print in the same line
        time.sleep(0.1)  # update every 0.1 seconds
except KeyboardInterrupt:
    print("\nExited.")
