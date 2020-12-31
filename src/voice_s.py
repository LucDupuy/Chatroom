import socket
import pyaudio
from threading import Thread

HOST = '0.0.0.0'
# HOST = socket.gethostbyname("ROGUEONE")
PORT = 80

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = RATE = 44100

# Works better when server side buffer is larger?
BUFFER_SIZE = 4096

p = pyaudio.PyAudio()
in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=BUFFER_SIZE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))


def get_data():
    while True:
        data, address = sock.recvfrom(BUFFER_SIZE)
        in_stream.write(data)


def send_data():
    while True:
        data, address = sock.recvfrom(BUFFER_SIZE)
        sock.sendto(data, address)


def main():
    get_thread = Thread(target=get_data())
    send_thread = Thread(target=send_data())
    get_thread.start()
    send_thread.start()
