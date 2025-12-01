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
from PyQt6.QtCore import Qt, QThread, pyqtSignal

import pyttsx3 # imported python text to speech engine
import speech_recognition as sr # for speech to text

# 
App_Name = "OculAurix" 

SPLASH_SCREEN_DURATION_MS = 3000

class TTSWorker(QThread):
    finished = pyqtSignal()
    
    def __init__(self,text,rate=80):
        super().__init__()
        self.text = text
        self.rate = rate
        
    def run(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', self.rate)
        engine.say(self.text)
        engine.runAndWait()
        self.finished.emit()
        
class STTWorker(QThread):
    result = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, recognizer):
        super().__init__()
        self.recognizer = recognizer
        self._running = True
        
    def run(self):
        import speech_recognition as sr
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
                if not self._running:
                    return
                text = self.recognizer.recognize_google(audio)
                self.result.emit(text)
        except sr.WaitTimeoutError:
                self.error.emit("No speech detected, try again.")
        except sr.UnknownValueError:
                self.error.emit("Sorry, I couldn't understand that.")
        except sr.RequestError:
            self.error.emit("Error: Speech recognition service unavailable.")
            
            def stop(self):
                self._running = False
                

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #speech recognizer
        self.recognizer = sr.Recognizer()
        self.tts_thread = None
        self.stt_thread = None
        
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
            # if tts thread is already running stop it first
            if self.tts_thread and self.tts_thread.isRunning():
                self.tts_thread.terminate()
                self.tts_thread = None
                
            self.label.setText("Speaking...")
            self.tts_thread = TTSWorker(text)
            self.tts_thread.finished.connect(lambda: self.label.setText("Enter text below:"))
            self.tts_thread.start()
        else:
            self.label.setText("Please type something first.")
        
    def clear_text(self):
        #Clear text box and reset label.
        self.text_input.clear()
        self.label.setText("Enter text below:")
        #stop tts
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.terminate()
            self.tts_thread = None
            
        #stop stt
        if self.stt_thread and self.stt_thread.isRunning():
            self.stt_thread.stop()
            self.stt_thread.terminate()
            self.stt_thread = None
            
            
    def handle_stt_result(self, text):
        self.text_input.setPlainText(text)
        self.label.setText("Speech Recognized Successfully")

        
    def speech_to_text(self):
        #Use microphone input to trancribe to text box
        self.label.setText("Listening...Speak Now.")
        self.stt_thread = STTWorker(self.recognizer)
        self.stt_thread.result.connect(self.handle_stt_result)
        self.stt_thread.error.connect(lambda msg: self.label.setText(msg))
        self.stt_thread.start()
        
        
                
#run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())