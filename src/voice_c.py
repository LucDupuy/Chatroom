import socket
import pyaudio
from threading import Thread

HOST = socket.gethostbyname("ROGUEONE")
PORT = 80

BUFFER_SIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100



def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((HOST, PORT))

    p = pyaudio.PyAudio()
    in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=BUFFER_SIZE)
    out_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER_SIZE)

    get_thread = Thread(target=get_data, args=(sock, in_stream))
    send_thread = Thread(target=send_data, args=(sock, out_stream))

    get_thread.start()
    send_thread.start()


def get_data(s, stream):
    while True:
        try:
            data, server = s.recvfrom(BUFFER_SIZE)
            stream.write(data)
        except socket.error:
            pass


def send_data(s, stream):
    while True:
        try:
            data = stream.read(BUFFER_SIZE)
            s.sendto(data, (HOST, PORT))
        except:
            pass


if __name__ == '__main__':
    main()
