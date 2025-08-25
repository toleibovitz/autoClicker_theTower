from game_loop import main_game_loop

from constants import *
from functions import *
import pyperclip
from typing import cast
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import sys
import threading
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel

APP = get_current_game_window()

class GameLoopThread(QThread):
    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()
        
    
    def run(self, window):
        main_game_loop(self.stop_event, window)

    def stop(self):
        self.stop_event.set()
        self.wait()


class AutoClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Tower - Auto Clicker")

        self.auto_clicker_button = QPushButton("Start Auto Clicker")
        self.auto_clicker_button.setCheckable(True)
        self.auto_clicker_button.clicked.connect(self.start_or_stop_game_loop)

        self.ad_gems_clicked_label = QLabel("Ad Gems Clicked")
        self.ad_gems_clicked_count = QLineEdit(readOnly=True)
        self.ad_gems_clicked_count.setText('0')

        self.current_gems_label = QLabel("Current Gems")
        self.current_gems = QLineEdit(readOnly=True)
        self.current_gems.setText('0')

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.ad_gems_clicked_label)
        h_layout.addWidget(self.ad_gems_clicked_count)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.auto_clicker_button)

        center = QWidget()
        center.setLayout(v_layout)
        self.setCentralWidget(center)

        self.game_thread = None

    def start_or_stop_game_loop(self, checked):
        if checked:
            self.auto_clicker_button.setText("Stop Auto Clicker")
            self.game_thread = GameLoopThread()
            self.game_thread.start(window)
        else:
            self.auto_clicker_button.setText("Start Auto Clicker")
            if self.game_thread:
                self.game_thread.stop()
                self.game_thread = None

    def update_ad_gems_clicked(self):
        current = self.ad_gems_clicked_count.text()
        current = int(current)
        current += 1
        self.ad_gems_clicked_count.setText(str(current))

    # def get_current_gems(self):
    #     coords = get_coords(APP, OFFSET_TOTAL_GEMS_AREA)
    #     check_area()




# def main_game_loop(stop_event):
    
#     retry_clicked = 0
#     ad_gem_clicked = 0
    
#     print(f"GAME NAME: {APP}")

#     while not stop_event.is_set():
#         loop_start = time.time()

#         # check if return to game is show
#         if check_area(APP, AreaLabel.RETURN_TO_GAME):
#             return_to_game_button_coords = get_coords(APP, OFFSET_MIDDLE_RETURN_TO_GAME)
#             move_and_click(return_to_game_button_coords, click=True)
#             continue
        
#         if not check_area(APP, AreaLabel.UPGRADE_MENU):
#             attack_upgrade_button_coords = get_coords(APP, OFFSET_ATTACK_UPGRADE_BUTTON)
#             move_and_click(attack_upgrade_button_coords, click=True)


#         # check if retry is shown
#         if check_area(APP, AreaLabel.NEW_HIGHEST_WAVE):
#             # move to more stats button
#                 more_stats_coords = get_coords(APP, OFFSET_MIDDLE_OF_MORE_STATS_BUTTON, additional_y_offset_needed=True, additional_y_offset=OFFSET_RATIO_NEW_HIGHEST_WAVE)
#                 move_and_click(more_stats_coords, click=True)

#                 # # copy round_stat
#                 copy_stats_button_coords = get_coords(APP, OFFSET_COPY_STATS)
#                 move_and_click(copy_stats_button_coords, click=True)
#                 round_stats = pyperclip.paste()
#                 save_round_stats("round_stats", round_stats)
                
#                 # # click outside of Round Stats
#                 outside_round_stats_coords = get_coords(APP, OFFSET_OUTSIDE_ROUND_STATS)
#                 move_and_click(outside_round_stats_coords, click=True)
                
#                 # # move to retry and click
#                 retry_button_coords = get_coords(APP, OFFSET_MIDDLE_OF_RETRY_BUTTON, additional_y_offset_needed=True, additional_y_offset=OFFSET_RATIO_NEW_HIGHEST_WAVE)
#                 move_and_click(retry_button_coords, click=True)
#                 retry_clicked += 1
#                 print(f"Retry Clicked {retry_clicked} time(s)")
#         if check_area(APP, AreaLabel.RETRY):
#             if check_area(APP, AreaLabel.MORE_STATS):
#                 # move to more stats button
#                 more_stats_coords = get_coords(APP, OFFSET_MIDDLE_OF_MORE_STATS_BUTTON)
#                 move_and_click(more_stats_coords, click=True)

#                 # copy round_stat
#                 copy_stats_button_coords = get_coords(APP, OFFSET_COPY_STATS)
#                 move_and_click(copy_stats_button_coords, click=True)
#                 round_stats = pyperclip.paste()
#                 save_round_stats("round_stats", round_stats)
                
#                 # click outside of Round Stats
#                 outside_round_stats_coords = get_coords(APP, OFFSET_OUTSIDE_ROUND_STATS)
#                 move_and_click(outside_round_stats_coords, click=True)
                
#                 # move to retry and click
#                 retry_button_coords = get_coords(APP, OFFSET_MIDDLE_OF_RETRY_BUTTON)
#                 move_and_click(retry_button_coords, click=True)
#                 retry_clicked += 1
#                 print(f"Retry Clicked {retry_clicked} time(s)")
        
#         # check if ad gem is shown
#         elif check_area(APP, AreaLabel.AD_GEM):
#             ad_gem_middle = get_coords(APP, OFFSET_MIDDLE_OF_AD_GEM_BUTTON)
#             # move_and_click(ad_gem_middle, click=True)
#             rect = get_window_dimension(APP, "rect")
#             height = cast(int, get_window_dimension(APP, dimension="height"))
#             big_radius = height * 0.10  # 20% of window height
#             click_circle(APP, rect, OFFSET_CENTER_OF_TOWER, big_radius, clicks=20, delay=0.001)
#             ad_gem_clicked += 1
#             window.update_ad_gems_clicked()
#             print(f"Ad Gem Clicked {ad_gem_clicked} time(s)")
#         else:
#             print(f"No Retry or Ad Gem found. Trying again in {RETRY_TIME} seconds...")
        
#         elapsed = time.time() - loop_start
#         remaining = RETRY_TIME - elapsed
#         if remaining > 0:
#             step = 0.1  # check every 0.1 sec
#             waited = 0
#             while waited < remaining:
#                 if stop_event.is_set():
#                     return
#                 time.sleep(step)
#                 waited += step




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClicker()
    
    window.show()
    
    sys.exit(app.exec())
