import socket
import sys
import threading
from threading import Thread
import pyaudio

HOST = "0.0.0.0"
PORT = 80
CHUNK = 1024
BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

