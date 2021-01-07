import requests
import tkinter.messagebox
import webbrowser
import pynput

from pynput import keyboard

text = ""
def on_press(key):
    try:
        text = key.char

        if key.char == "q":
            print(text)

        #special keys
    except AttributeError:
        pass



# Collect events until released
with keyboard.Listener(
        on_press=on_press,  suppress=True) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,  suppress=True)
listener.start()

# https://ilkka.ddns.net/LukiChat/version.txt
# http://192.168.2.239/LukiChat/version.txt
