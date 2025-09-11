from typing import Tuple, Union, Literal
import win32gui
import pyautogui
from PIL import ImageGrab
import pytesseract
import time
import mss, mss.tools
import numpy as np
from datetime import datetime, timedelta, timezone
import math
import csv
from src.constants import AREAS, AreaLabel
from icecream import ic


def get_current_game_window() -> str:
    windows = pyautogui.getAllWindows()
    results = []
    name = "BlueStacks App Player"
    for window in windows:
        if name in window.title:
            results.append(window.title)

    if len(results) == 1:
        return results[0] 
    else:
        raise ValueError("Too many windows found. Please only have one open window.")


def move_and_click(
        coords: Union[tuple, None],  
        click: bool = True, 
        corner: Literal["top_left", "bottom_right"] = "top_left"
        ) -> None:
    
    """
    Move the mouse to a given coordinate or rectangle and optionally click.

    - (x, y): moves to the point, and clicks if `click=True`.
    - (x1, y1, x2, y2): moves to one corner, but never clicks.

    Args:
        coords: (x, y) for a point OR (x1, y1, x2, y2) for a rectangle.
        click: Whether to click after moving (ignored for rectangle).
        corner: Which part of the rectangle to move to ("top_left" or "bottom_right").
    """
    if coords is None:
        print("No coordinates provided.")
        return
    
    if len(coords) == 2:
        pyautogui.moveTo(coords)
        if click:
            pyautogui.click()
    elif len(coords) == 4:
        if corner == "top_left":
            pyautogui.moveTo(coords[0], coords[1])
        elif corner == "bottom_right":
            pyautogui.moveTo(coords[2], coords[3])


def get_coords(
        app: str, 
        offsets: tuple,
        additional_x_offset_needed: bool = False,
        additional_y_offset_needed: bool = False,
        additional_x_offset: float = 1.0,
        additional_y_offset: float = 1.0,  
        ) -> Union[Tuple[int, int], Tuple[int, int, int, int], None]:
    
    """
    Get coordinates inside a window based on relative offsets.

    Args:
        app: Window title (case-sensitive) to search for.
        offsets: Either:
            - (x_ratio, y_ratio) for a single point
            - (x1_ratio, y1_ratio, x2_ratio, y2_ratio) for a rectangle
        additional_x_offset_needed: Whether to apply scaling to X ratio.
        additional_y_offset_needed: Whether to apply scaling to Y ratio.
        additional_x_offset: Multiplier applied to X ratio.
        additional_y_offset: Multiplier applied to Y ratio.

    Returns:
        (x, y) if 2 offsets were given,
        (x1, y1, x2, y2) if 4 offsets were given,
        None if window not found.
    """
    
    hwnd = win32gui.FindWindow(None, app)
    
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top

        x = round(left + (width * offsets[0]))
        y = round(top + height * offsets[1])
        
        if len(offsets) == 2:
            if additional_x_offset_needed:
                x *= additional_x_offset
            if additional_y_offset_needed:
                y *= additional_y_offset
            return (x, y)
        
        elif len(offsets) == 4:
            x1 = round(left + (width * offsets[0]))
            y1 = round(top + height * offsets[1])
            x2 = round(left + (width * offsets[2]))
            y2 = round(top + height * offsets[3])
            if additional_x_offset_needed:
                x1 *= additional_x_offset
                x2 *= additional_x_offset
            if additional_y_offset_needed:
                y1 *= additional_y_offset
                y2 *= additional_y_offset  
            return (x1, y1, x2, y2)
    
    return None



def get_window_dimension(
        app: str, 
        dimension: Literal["all", "rect", "height", "width"]
        ) -> Union[Tuple[int, int, int, int], Tuple[Tuple[int, int, int, int], int, int], int, None]:
    
    """
    Retrieve dimensions of a window by its title.

    Args:
        app (str): The window title (case-sensitive).
        dimension (Literal["all", "rect", "height", "width"]): 
            - "all": Returns (rect, height, width).
            - "rect": Returns the full window rectangle (left, top, right, bottom).
            - "height": Returns only the window height.
            - "width": Returns only the window width.

    Returns:
        Union:
            - Tuple[Tuple[int, int, int, int], int, int]: If "all".
            - Tuple[int, int, int, int]: If "rect".
            - int: If "height" or "width".
            - None: If the window is not found.
    """
    
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



def capture_region_and_check(coords, text_to_look_for, text_to_print):
    
    """
    Capture a screen region and check for a specific text using OCR.

    Args:
        coords (tuple): Screen region as (left, top, right, bottom).
        text_to_look_for (str): Text to search for in the captured image.
        text_to_print (str): Label used in printed messages.

    Returns:
        bool: True if the text is found, False otherwise.
    """
    
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
    
    if text_to_look_for in text_read.strip():
        print(f"{text_to_print} Found")
        return True
    else:
        print(f"{text_to_print} NOT Found")
        return False


def save_round_stats(file_path, data):
    
    """
    Save round statistics to a CSV file with a timestamped filename.

    Args:
        file_path (str): Directory where the CSV file should be saved.
        data (str): Raw stats data as tab-delimited lines.

    Side Effects:
        Creates a CSV file in the specified directory. 
        The filename includes the current timestamp (CST, UTC-6).
        Prints an exception message if file saving fails.
    """
    
    lines = data.strip().split("\n")
    rows = [line.split("\t") for line in lines]
    tz_offset = timezone(timedelta(hours=-6))
    now = datetime.now(tz_offset).strftime('%Y-%m-%d-%H-%M-%S')
    
    file_path += f"/{now}.csv"
    

    try:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Stat", "Value"])
            writer.writerows(rows)
    except Exception as e:
        print(e)

def click_circle(app, bounds, tower_center, radius_px, clicks=8, delay=0.1):
    
    """
    Simulate mouse clicks in a circular pattern around a tower center.

    Args:
        bounds (tuple): Not currently used (kept for compatibility).
        tower_center (tuple): Relative tower center as (x_ratio, y_ratio).
        radius_px (int): Radius of the circle in pixels.
        clicks (int, optional): Number of clicks around the circle. Default is 8.
        delay (float, optional): Delay between clicks in seconds. Default is 0.1.

    Side Effects:
        Moves the mouse and performs clicks using pyautogui.
    """

    rect, height, width =  get_window_dimension(app, dimension="all")
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


def check_area(app: str, label: AreaLabel) -> bool:
    
    """
    Check a predefined screen area for specific text.

    Args:
        label (AreaLabel): The area label defined in AREAS mapping.

    Returns:
        bool: True if the text associated with the area is found, False otherwise.
    """
    


    offsets, text = AREAS[label]
    coords = get_coords(app, offsets)
    return capture_region_and_check(coords, text, label)


def take_screen_shot(coords, fname):
    left, top, right, bottom = coords
    width = right - left
    height = bottom - top
    
    
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        image = sct.grab(monitor)
        mss.tools.to_png(image.rgb, image.size, output=f"{fname}.png")