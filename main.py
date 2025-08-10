import win32gui
import win32api
import win32con
import win32print
import pyautogui
from PIL import ImageGrab
import pytesseract
import time
import mss
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def enum_window_titles():
    windows = []
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))
    win32gui.EnumWindows(callback, None)
    return windows

def get_monitor_for_window(hwnd):
    hmonitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    info = win32api.GetMonitorInfo(hmonitor)
    return info

# this get the middle of the ad gem button
def get_middle_position_ad_gem():
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        
        left, top, right, bottom = rect
        width = right - left
        x_ad_gem = left + (width * .15)
        y_ad_gem = top + (bottom - top) * .44

        ad_gem_coords = (x_ad_gem, y_ad_gem)
        return ad_gem_coords
    else:
        return None


# bbox = (left, top, right, bottom)
# this gets left, top, right and bottom of the ad gem button
def get_ad_gem_area():
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        
        left, top, right, bottom = rect
        width = right - left
        
        
        left_x = round(left + (width * .03))
        right_x = round(left + (width * .23))

        top_y = round(top + (bottom - top) * .40)
        bottom_y = round(top + (bottom - top) * .47)

        
        return (left_x, top_y, right_x, bottom_y)


def get_middle_position_retry():
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        
        left, top, right, bottom = rect
        width = right - left


def get_retry_button_area():
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        
        left, top, right, bottom = rect
        width = right - left

        left_x = round(left + (width * .03))
        right_x = round(left + (width * .23))

        top_y = round(top + (bottom - top) * .40)
        bottom_y = round(top + (bottom - top) * .47) 

        return (left_x, top_y, right_x, bottom_y)




def capture_region_and_check():
    coords = get_ad_gem_area()
    if not coords:
        print("Window not found.")
        return False

    left, top, right, bottom = coords
    width = right - left
    height = bottom - top

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        img = np.array(sct.grab(monitor))

    
    # gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    
    text = pytesseract.image_to_string(img)
    
    print("Detected text:", text.strip())

    return "CLAIM" in text  

def main():
    coords = get_retry_button_area()

    pyautogui.moveTo()
    # while True:
    #     if capture_region_and_check():
    #         print("Found Target Text")
    #         coords = get_middle_position_ad_gem()
    #         pyautogui.moveTo(coords)
    #         pyautogui.click()

    #     else:
    #         print("Nothing Found")
    #     time.sleep(60)
    



if __name__ == "__main__":
    main()

      