from game_loop import main_game_loop
from constants import *
from functions import *
import pyperclip
from typing import cast
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import sys
import threading
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel


class GameLoopThread(QThread):
    ad_gem_clicked = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()
        

    def run(self):
        event_handlers = {
            "ad_gem_clicked": lambda payload: self.ad_gem_clicked.emit(int(payload.get("count", 0)))
        }

        def notify(event: str, payload: dict):
            handler = event_handlers.get(event)
            if handler:
                handler(payload)

        main_game_loop(self.stop_event, notify)

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
            self.game_thread.ad_gem_clicked.connect(self.on_ad_gem_clicked)
            self.game_thread.start()
        else:
            self.auto_clicker_button.setText("Start Auto Clicker")
            if self.game_thread:
                self.game_thread.stop()
                self.game_thread = None

    def on_ad_gem_clicked(self, count: int):
        self.ad_gems_clicked_count.setText(str(count))

    # def get_current_gems(self):
    #     coords = get_coords(APP, OFFSET_TOTAL_GEMS_AREA)
    #     check_area()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClicker()
    
    window.show()
    
    sys.exit(app.exec())




