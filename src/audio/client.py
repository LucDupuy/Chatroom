import socket
import sys
import threading
from threading import Thread
import pyaudio
import sounddevice as sd
import numpy as np


CHUNK = 1024
BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# HOST = socket.gethostbyname("ilkka.ddns.net")
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80

