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

from PyQt6.QtGui import QIcon

import pyttsx3 # 

# 
App_Name = "OculAurix" 

SPLASH_SCREEN_DURATION_MS = 3000

tts_engine = pyttsx3.init()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("OculAurix: ")
        self.setGeometry(50,50,600,500)
        #self.setWindowIcon()
        
        
app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())