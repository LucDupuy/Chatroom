import socket
import pyaudio
import tkinter
from tkinter import messagebox

HOST = socket.gethostbyname("ROGUEONE")
PORT = 80

BUFFER_SIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


client_sock = socket.socket()

try:
    client_sock.connect((HOST, PORT))
except:
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.withdraw()
    tkinter.messagebox.showinfo("Error", "Server is offline")
    exit(0)


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=BUFFER_SIZE)


while True:
    data = client_sock.recv(BUFFER_SIZE)
    stream.write(data)