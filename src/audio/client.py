import socket
import sys
import threading
import tkinter
import tkinter.messagebox
from threading import Thread
import pyaudio
import sounddevice as sd
import numpy as np

CHUNK = 1024 * 2
BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# HOST = socket.gethostbyname("ilkka.ddns.net")
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def client():
    p = pyaudio.PyAudio()
    stream = p.open(format=BIT_DEPTH, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    with socket.socket() as client_socket:
        client_socket.connect((HOST, PORT))
        print(client_socket.recv(2048).decode('utf-8'))
        while True:
            data = client_socket.recv(CHUNK)
            stream.write(data)


if __name__ == "__main__":
    client()
