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
        
    def run(self):
        main_game_loop(self.stop_event)

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
            self.game_thread.start()
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClicker()
    
    window.show()
    
    sys.exit(app.exec())




