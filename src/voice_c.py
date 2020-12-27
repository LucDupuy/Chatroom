import pyaudio
import socket
from threading import Thread

HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

frames = []


def udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        if len(frames) > 0:
            sock.sendto(frames.pop(0), (HOST, PORT))


def record(stream, CHUNK):
    while True:
        frames.append(stream.read(CHUNK))


if __name__ == "__main__":
    p = pyaudio.PyAudio()
    in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=False, frames_per_buffer=BUFFER_SIZE)

    rec_thread = Thread(target=record, args=(in_stream, BUFFER_SIZE, ))
    rec_thread.setDaemon(True)
    rec_thread.start()
    rec_thread.join()

    udp_thread = Thread(target=udp)
    udp_thread.setDaemon(True)
    udp_thread.start()
    udp_thread.join()
