import win32gui
import pyautogui
from PIL import ImageGrab
import pytesseract
import time
import mss, mss.tools
import numpy as np
from datetime import datetime, timedelta, timezone
import math

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Constants
# (x, y) or (left, top, right, bottom)

APP = "BlueStacks App Player"

# seconds
RETRY_TIME = 120

OFFSET_MIDDLE_OF_AD_GEM_BUTTON = (.15, .44)
OFFSET_AD_GEM_AREA = (.03, .40, .23, .47)

OFFSET_MIDDLE_OF_RETRY_BUTTON = (.25, .74)
OFFSET_RETRY_BUTTON_AREA = (.09, .71, .45, .77)

OFFSET_MIDDLE_OF_MORE_STATS_BUTTON = (.32, .54)
OFFSET_MORE_STATS_AREA = (.19, .52, .46, .565)

OFFSET_ROUND_STATS_AREA = (.1, .12, .87, .88)
OFFSET_ROUND_STATS_BOTTOM = (.5, .83)
OFFSET_ROUND_STATS_TOP = (.5, .22)
OFFSET_OUTSIDE_ROUND_STATS = (.5, .08)

OFFSET_DRAG_DISTANCE = .56

OFFSET_RETURN_TO_GAME_AREA = (.17, .92, .8, .97)
OFFSET_MIDDLE_RETURN_TO_GAME = (.5, .945)

OFFSET_FLOATIING_DIAMOND_AREA = (.3, .15, .67, .37)

OFFSET_CENTER_OF_TOWER = (.485,.255)

# takes a set of offsets and returns a tuple of coordinates
def get_coords(app, offsets: tuple) -> tuple:
    hwnd = win32gui.FindWindow(None, app)

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left

        if len(offsets) == 2:
            x = round(left + (width * offsets[0]))
            y = round(top + (bottom - top) * offsets[1])

            middle_of_area = (x, y)
            
            return middle_of_area
        elif len(offsets) == 4:
            left_x = round(left + (width * offsets[0]))
            top_y = round(top + (bottom - top) * offsets[1])
            right_x = round(left + (width * offsets[2]))
            bottom_y = round(top + (bottom - top) * offsets[3])

            coords_of_area = (left_x, top_y, right_x, bottom_y)
            return coords_of_area
    
    return ()



def get_window_dimension(app, dimension):
    hwnd = win32gui.FindWindow(None, app)

    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
    else:
        print("Something went wrong and this window cannot be found")
    
    left, top, right, bottom = rect
    height = bottom - top
    width = right - left
    if dimension == "all":
        return rect, height, width
    elif dimension == "rect":
        return rect
    elif dimension == "height":
        return height
    elif dimension == "width":
        return width



def capture_region_and_check(coords, text, text_to_print):
    if not coords:
        print("Window not found.")
        return False

    left, top, right, bottom = coords
    width = right - left
    height = bottom - top

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        img = np.array(sct.grab(monitor))
        
            
    text_read = pytesseract.image_to_string(img)
    
    if text in text_read.strip():
        print(f"{text_to_print} Found")
        return True
    else:
        print(f"{text_to_print} NOT Found")
        return False



def take_screen_shot(coords, fname):
    left, top, right, bottom = coords
    width = right - left
    height = bottom - top
    tz_offset = timezone(timedelta(hours=-6))
    now = datetime.now(tz_offset).strftime('%Y-%m-%d-%H-%M-%S')
    

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        image = sct.grab(monitor)
        mss.tools.to_png(image.rgb, image.size, output=f"{fname}_{now}.png")


def click_circle(bounds, tower_center, radius_px, clicks=8, delay=0.1):
    
    rect, height, width =  get_window_dimension(APP, dimension="all")
    left, top, right, bottom = rect
    tower_x = left + tower_center[0] * width
    tower_y = top + tower_center[1] * height

    for i in range(clicks):
        angle = (2 * math.pi / clicks) * i
        x = tower_x + math.cos(angle) * radius_px
        y = tower_y + math.sin(angle) * radius_px
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(delay)


def main():
    retry_text = "RETRY"
    ad_gem_text = "CLAIM"
    more_stats_text = "MORE STATS"
    return_to_game_text = "Tap To Return To Game"
    retry_clicked = 0
    ad_gem_clicked = 0


    while True:
        retry_coords = get_coords(APP, OFFSET_RETRY_BUTTON_AREA)
        is_retry_shown = capture_region_and_check(retry_coords, retry_text, "RETRY" )
        
        return_to_game_coords = get_coords(APP, OFFSET_RETURN_TO_GAME_AREA)
        is_return_to_game_shown = capture_region_and_check(return_to_game_coords, return_to_game_text, "RETURN TO GAME")
        
        
        
        # check if return to game is show
        if is_return_to_game_shown:
            pyautogui.moveTo(get_coords(APP, OFFSET_MIDDLE_RETURN_TO_GAME))
            pyautogui.click()    
        # check if retry is shown
        elif is_retry_shown:
            more_stats_coords = get_coords(APP, OFFSET_MORE_STATS_AREA)
            more_stats_shown = capture_region_and_check(more_stats_coords, more_stats_text, "MORE STATS")
            print(f"MORE STATS SHOW: {more_stats_shown}")
            if more_stats_shown:
                # move to more stats button
                more_stats_coords = get_coords(APP, OFFSET_MIDDLE_OF_MORE_STATS_BUTTON)
                pyautogui.moveTo(more_stats_coords)
                pyautogui.click()

                # reset round stats by dragging back up
                pyautogui.moveTo(get_coords(APP, OFFSET_ROUND_STATS_TOP))
                height = get_window_dimension(APP, "height")
                drag_offset = round(height * OFFSET_DRAG_DISTANCE)
                pyautogui.drag(0, drag_offset, duration=1.5, button="left")
                pyautogui.moveTo(get_coords(APP, OFFSET_ROUND_STATS_TOP))
                pyautogui.drag(0, drag_offset, duration=1.5, button="left")
                
                # take screen shot
                time.sleep(2)
                take_screen_shot(get_coords(APP, OFFSET_ROUND_STATS_AREA), "round_stats")
                
                #drag down
                pyautogui.moveTo(get_coords(APP, OFFSET_ROUND_STATS_BOTTOM))
                pyautogui.drag(0, -drag_offset, duration=2.5, button="left")
                time.sleep(2)

                # take another screen shot
                take_screen_shot(get_coords(APP, OFFSET_ROUND_STATS_AREA), "round_stats")  

                # drag down
                pyautogui.moveTo(get_coords(APP, OFFSET_ROUND_STATS_BOTTOM))
                pyautogui.drag(0, -drag_offset, duration=2.5, button="left")
                time.sleep(2)  

                # take last screen shot
                take_screen_shot(get_coords(APP, OFFSET_ROUND_STATS_AREA), "round_stats") 
                
                # click outside of Round Stats
                pyautogui.moveTo(get_coords(APP, OFFSET_OUTSIDE_ROUND_STATS))
                pyautogui.click()
                # move to retry and click
                pyautogui.moveTo(get_coords(APP, OFFSET_MIDDLE_OF_RETRY_BUTTON))
                pyautogui.click()

                
                
                retry_clicked += 1
                print(f"Retry Clicked {retry_clicked} time(s)")
        # check if ad gem is shown
        elif capture_region_and_check(get_coords(APP, OFFSET_AD_GEM_AREA), ad_gem_text, "AD GEM CLAIM"):
            ad_gem_middle = get_coords(APP, OFFSET_MIDDLE_OF_AD_GEM_BUTTON)
            pyautogui.moveTo(ad_gem_middle)
            pyautogui.click()
            rect = get_window_dimension(APP, "rect")
            height = get_window_dimension(APP, dimension="height")
            big_radius = height * 0.10  # 20% of window height
            click_circle(rect, OFFSET_CENTER_OF_TOWER, big_radius, clicks=20, delay=0.001)
            ad_gem_clicked += 1
            print(f"Ad Gem Clicked {ad_gem_clicked} time(s)")
        else:
            print(f"No Retry or Ad Gem found. Trying again in {RETRY_TIME} seconds...")
        time.sleep(RETRY_TIME)

    
    


if __name__ == "__main__":
    main()

      