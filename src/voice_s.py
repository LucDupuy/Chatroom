import socket
import pyaudio
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 80
NUM_CONNECTIONS = 5
BUFFER_SIZE = 2048

BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((HOST, PORT))

p = pyaudio.PyAudio()
stream = p.open(format=BIT_DEPTH, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER_SIZE)


while True:
    data, addr = s.recvfrom(BUFFER_SIZE)
    if addr not in clients:
        clients.append(addr)

    for client in clients:
        if client != addr:
            s.sendto(data, client)






