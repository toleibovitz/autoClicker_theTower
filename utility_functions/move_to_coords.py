import pyautogui
import win32gui
import mss, mss.tools

APP = "BlueStacks App Player"

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

OFFSET_RETURN_TO_GAME_AREA = (.17, .92, .8, .97)
OFFSET_MIDDLE_RETURN_TO_GAME = (.5, .945)

OFFSET_FLOATIING_DIAMOND_AREA = (.3,.25,.2,.2)

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
            pyautogui.moveTo(middle_of_area)
            return middle_of_area
        elif len(offsets) == 4:
            left_x = round(left + (width * offsets[0]))
            top_y = round(top + (bottom - top) * offsets[1])
            right_x = round(left + (width * offsets[2]))
            bottom_y = round(top + (bottom - top) * offsets[3])

            coords_of_area = (left_x, top_y, right_x, bottom_y)
            pyautogui.moveTo(coords_of_area[0], coords_of_area[1])
            return coords_of_area
    
    return ()

get_coords(APP, OFFSET_FLOATIING_DIAMOND_AREA)


# left, top, right, bottom = round_stats_area
# width = right - left
# height = bottom - top

# with mss.mss() as sct:
#     monitor = {"top": top, "left": left, "width": width, "height": height}
#     image = sct.grab(monitor)
#     mss.tools.to_png(image.rgb, image.size, output="round_stats.png")
