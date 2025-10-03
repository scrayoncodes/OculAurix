#
import sys;
#
from PyQt6.QtWidgets import ( # imported tools needed to create structure of the app
    QApplication,
    QMainWindow, 
    QWidget,
    QVBoxLayout, 
    QPushButton, 
    QTextEdit,
    QLabel
)

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

import pyttsx3 # imported python text to speech engine
import speech_recognition as sr # for speech to text

# 
App_Name = "OculAurix" 

SPLASH_SCREEN_DURATION_MS = 3000

tts_engine = pyttsx3.init()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # window setup
        self.setWindowTitle("OculAurix")
        self.setGeometry(50,50,600,500)
        #self.setWindowIcon(QIcon("Downloads/OculAurix Logo.png"))
        
        #central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        #layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        #label
        self.label = QLabel("Enter text below:")
        layout.addWidget(self.label)
        
        #text box
        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)
        
        #speak button
        self.speak_button = QPushButton("Speak Text")
        self.speak_button.clicked.connect(self.speak_text)
        layout.addWidget(self.speak_button)
        
    def speak_text(self):
        #Take input from text and read it out
        text = self.text_input.toPlainText()
        if text.strip():
            tts_engine.say(text)
            tts_engine.runAndWait()
        else:
            self.label.setText("Please type something first.")
        
        
#run the app
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())