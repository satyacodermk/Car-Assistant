import pyttsx3 as ptsx
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
#from home_gui import *
# making engine globally available

engine = ptsx.init()
engine.setProperty("rate", 150)  # default rate of voice
engine.setProperty("volume",1.0)

# ============================= Greeting the user or Welcome user ============
def greetUser(name=""):
    text=name+" Welcome to the system 3.10 my name is carvis "
    speak(text)
# ============================= Saying By to the user ========================
def byfun(name=""):
    print("Bye ... ",name)
    text="By It was nice experience with you"+name
    speak(text)
def speak(text):
    # say function is used to add a word to speak to the queue, while the runAndWait() method runs the real event loop until all commands queued up
    engine.say(text)
    # play the speech
    engine.runAndWait()

if __name__=='__main__':
    mode="Traffic Recognizer"
    gui_carvis(mode)