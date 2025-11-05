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
tts_rate = tts_engine.getProperty('rate')
tts_engine.setProperty('rate',80)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #speech recognizer
        self.recognizer = sr.Recognizer()
        
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
        
        #clear button
        self.clear_button = QPushButton("Clear Text")
        self.clear_button.clicked.connect(self.clear_text)
        layout.addWidget(self.clear_button)
        
        #listen button
        self.listen_button = QPushButton("Speech to Text")
        self.listen_button.clicked.connect(self.speech_to_text)
        layout.addWidget(self.listen_button)
        
    def speak_text(self):
        #Take input from text and read it out
        text = self.text_input.toPlainText().strip()
        if text:
            self.label.setText("Speaking...")
            # initialize engine fresh every time to stop freezing
            tts_engine = pyttsx3.init()
            tts_engine.setProperty('rate', 80)
            tts_engine.say(text)
            tts_engine.runAndWait()
            tts_engine.stop()
            
            self.label.setText("Enter text below:")
        else:
            self.label.setText("Please type something first.")
        
    def clear_text(self):
        #Clear text box and reset label.
        self.text_input.clear()
        self.label.setText("Enter text below:")
    
    

    def speech_to_text(self):
        #Use microphone input to trancribe to text box
        self.label.setText("Listening...Speak Now.")
        
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source,timeout=5)
                text = self.recognizer.recognize_google(audio)
                self.text_input.setPlainText(text)
                self.label.setText("Speech Recognized Successfully")
        except sr.WaitTimeoutError:
                self.label.setText("No speech detected, try again.")
        except sr.UnknownValueError:
                self.label.setText("Sorry, I couldn't understand that.")
        except sr.RequestError:
            self.label.setText("Error: Speech recognition service unavailable.")
                
#run the app
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())