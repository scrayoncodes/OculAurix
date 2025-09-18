#
import sys;
# 
from PyQt6.QtWidgets import (
    QApplication, #
    QWidget, #
    QPushButton, #
    QVBoxLayout, # 
    QLineEdit, #
    QLabel, #
    QSplashScreen #
)
# 
from PyQt6.QtGui import(
    QFont, #
    QPixmap, #
)
# 
from PyQt6.QtCore import(
    Qt, #
    QTimer, #
    QCoreApplication, #
)

# 
import pyttsx3 # 

# 
App_Name = "OculAurix" 

SPLASH_SCREEN_DURATION_MS = 3000

tts_engine = pyttsx3.init()