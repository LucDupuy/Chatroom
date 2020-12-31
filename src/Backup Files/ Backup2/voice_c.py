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
frames_to_play = []


def get_data(udp_sock):
    pass


def send(udp_sock):
    while True:
        if len(frames) > 0:
            udp_sock.sendto(frames.pop(0), (HOST, PORT))


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

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    rec_thread = Thread(target=record_voice, args=(in_stream, BUFFER_SIZE))
    send_thread = Thread(target=send, args=(sock,))
    get_thread = Thread(target=get_data, args=(sock,))

    rec_thread.start()
    send_thread.start()
    get_thread.start()
    rec_thread.join()
    send_thread.join()
    get_thread.join()


if __name__ == '__main__':
    main()
