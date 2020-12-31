import socket
import pyaudio
from threading import Thread

HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((HOST, PORT))

BUFFER_SIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=BUFFER_SIZE)
out_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER_SIZE)


def get_data():
    while True:
        try:
            data, server = s.recvfrom(BUFFER_SIZE)
            in_stream.write(data)
        except socket.error:
            pass


def send_data():
    while True:
        try:
            data = out_stream.read(BUFFER_SIZE)
            s.sendto(data, (HOST, PORT))
        except:
            pass


get_thread = Thread(target=get_data)
send_thread = Thread(target=send_data)

get_thread.start()
send_thread.start()

