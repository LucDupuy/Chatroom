import pyaudio
import socket
from threading import Thread

# HOST = "192.168.2.106"
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80

BUFFER_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
frames = []


def udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        if len(frames) > 0:
            sock.sendto(frames.pop(0), (HOST, PORT))


def record_voice(stream, CHUNK):
    while True:
        frames.append(stream.read(CHUNK))


def play(stream, CHUNK):
    BUFFER = 10
    while True:
        if len(frames) == BUFFER:
            while True:
                try:
                    stream.write(frames.pop(0), CHUNK)
                except IndexError as e:
                    pass


def main():
    p = pyaudio.PyAudio()
    in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER_SIZE)

    rec_thread = Thread(target=record_voice, args=(in_stream, BUFFER_SIZE,))
    socket_thread = Thread(target=udp)

    rec_thread.start()
    socket_thread.start()
    rec_thread.join()
    socket_thread.join()


if __name__ == '__main__':
    main()
