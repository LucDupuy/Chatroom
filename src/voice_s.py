import pyaudio
import socket
from threading import Thread

HOST = '0.0.0.0'
# HOST = socket.gethostbyname("ROGUEONE")
PORT = 80

FORMAT = pyaudio.paInt16
BUFFER_SIZE = 1024
CHANNELS = 2
RATE = 44100

frames = []


def udpStream(CHUNK):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((HOST, PORT))

    while True:
        soundData, addr = udp.recvfrom(CHUNK * CHANNELS * 2)
        frames.append(soundData)


def play(stream, CHUNK):
    BUFFER = 10
    while True:
        if len(frames) == BUFFER:
            while True:
                stream.write(frames.pop(0), CHUNK)


if __name__ == "__main__":
    p = pyaudio.PyAudio()
    out_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=BUFFER_SIZE)

    socket_thread = Thread(target=udpStream, args=(BUFFER_SIZE,))
    sending_thread = Thread(target=play, args=(out_stream, BUFFER_SIZE,))
    
    socket_thread.start()
    sending_thread.start()
    socket_thread.join()
    sending_thread.join()
