from game_loop import main_game_loop

import sys
import threading
from PySide6.QtCore import QSize, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton



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

        self.button = QPushButton("Start Auto Clicker")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.start_or_stop_game_loop)

        self.setCentralWidget(self.button)
        self.setFixedSize(QSize(800, 600))

        self.game_thread = None

    def start_or_stop_game_loop(self, checked):
        if checked:
            self.button.setText("Stop Auto Clicker")
            self.game_thread = GameLoopThread()
            self.game_thread.start()
        else:
            self.button.setText("Start Auto Clicker")
            if self.game_thread:
                self.game_thread.stop()
                self.game_thread = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClicker()
    window.show()
    sys.exit(app.exec())
