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

# def enum_window_titles():
#     windows = []
#     def callback(hwnd, extra):
#         if win32gui.IsWindowVisible(hwnd):
#             title = win32gui.GetWindowText(hwnd)
#             if title:
#                 windows.append((hwnd, title))
#     win32gui.EnumWindows(callback, None)
#     return windows

# def get_monitor_for_window(hwnd):
#     hmonitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
#     info = win32api.GetMonitorInfo(hmonitor)
#     return info

# this get the middle of the ad gem button
def get_middle_position_ad_gem():
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        
        left, top, right, bottom = rect
        width = right - left
        x_ad_gem = round(left + (width * .15))
        y_ad_gem = round(top + (bottom - top) * .44)

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
        x_retry = round(left + (width * .25))
        y_retry = round(top + (bottom - top) * .74)

        retry_button_middle_coords = (x_retry, y_retry)
        return retry_button_middle_coords


def get_retry_button_area():
    hwnd = win32gui.FindWindow(None, "BlueStacks App Player")

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        
        left, top, right, bottom = rect
        width = right - left

        left_x = round(left + (width * .09))
        top_y = round(top + (bottom - top) * .71)
        
        
        right_x = round(left + (width * .45))
        bottom_y = round(top + (bottom - top) * .77) 

        return (left_x, top_y, right_x, bottom_y)




def capture_region_and_check(coords, text, text_to_find):
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

    
    text_read = pytesseract.image_to_string(img)
    
    if text in text_read.strip():
        print(f"{text_to_find} Found")
        return True
    else:
        print(f"{text_to_find} NOT Found")
        return False

     

def main():
    retry_text = "RETRY"
    ad_gem_text = "CLAIM"
    retry_clicked = 0
    ad_gem_clicked = 0


    while True:
        retry_coords = get_retry_button_area()
        is_retry_shown = capture_region_and_check(retry_coords, retry_text, "RETRY" )
        
        if is_retry_shown:
            retry_button_middle_coords = get_middle_position_retry()
            pyautogui.moveTo(retry_button_middle_coords)
            pyautogui.click()
            retry_clicked += 1
            print(f"Retry Clicked {retry_clicked} time(s)")
        elif capture_region_and_check(get_ad_gem_area(), ad_gem_text, "AD GEM CLAIM"):
            ad_gem_middle = get_middle_position_ad_gem()
            pyautogui.moveTo(ad_gem_middle)
            pyautogui.click()
            ad_gem_clicked += 1
            print(f"Ad Gem Clicked {ad_gem_clicked} time(s)")
        else:
            print("No Retry or Ad Gem found. Trying again in 120 seconds...")
        time.sleep(120)

    
    


if __name__ == "__main__":
    main()

      