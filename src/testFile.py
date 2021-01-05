import requests
import tkinter.messagebox
import webbrowser

VERSION = "0.5"

response = requests.get("https://ilkka.ddns.net/LukiChat/version.txt")
data = response.text

if data > VERSION:
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.withdraw()
    response = tkinter.messagebox.askyesno("Update", "Update available, would you like to download?")

    if response:
        webbrowser.open("https://ilkka.ddns.net/LukiChat/")
    else:
        pass

else:
    pass


# https://ilkka.ddns.net/LukiChat/version.txt
# http://192.168.2.239/LukiChat/version.txt
