import pyaudio
import socket
from threading import Thread

HOST = '0.0.0.0'
# HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

frames = []


def udp(CHUNK):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    while True:
        msg, addr = sock.recvfrom(CHUNK)
        frames.append(msg)


def play_voice(stream, CHUNK):
    BUFFER = 10
    while True:
        if len(frames) == BUFFER:
            while True:
                print(frames.pop(0))
#                stream.write(frames.pop(0), CHUNK)


if __name__ == "__main__":
    p = pyaudio.PyAudio()
    out_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=False, output=True, frames_per_buffer=BUFFER_SIZE)

    udp_thread = Thread(target=udp, args=(BUFFER_SIZE,))
    udp_thread.setDaemon(True)
    udp_thread.start()
    udp_thread.join()

    play_thread = Thread(target=play_voice, args=(out_stream, BUFFER_SIZE,))
    play_thread.setDaemon(True)
    play_thread.start()
    play_thread.join()
