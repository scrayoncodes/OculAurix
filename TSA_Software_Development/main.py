#
import sys;
# 
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow, #
    QWidget, #
    QPushButton, #
    QLabel, #
)

import pyttsx3 # 

# 
App_Name = "OculAurix" 

SPLASH_SCREEN_DURATION_MS = 3000

tts_engine = pyttsx3.init()

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("OculAurix: ")
window.show()

sys.exit(app.exec())