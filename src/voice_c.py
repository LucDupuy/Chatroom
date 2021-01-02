import socket
import pyaudio
from threading import Thread

HOST = socket.gethostbyname("ROGUEONE")
PORT = 1128

BUFFER_SIZE_SEND = 1024
BUFFER_SIZE_RECEIVE = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((HOST, PORT))

    p = pyaudio.PyAudio()
    in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=BUFFER_SIZE_SEND)
    out_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER_SIZE_SEND)




    get_thread = Thread(target=get_data, args=(sock, in_stream))
    send_thread = Thread(target=send_data, args=(sock, out_stream))

    get_thread.start()
    send_thread.start()


def get_data(s, stream):
    while True:
        try:
            data, server = s.recvfrom(BUFFER_SIZE_RECEIVE)
            stream.write(data)
        except socket.error as e:
            print(e)
            pass


def send_data(s, stream):
    while True:
        try:
            data = stream.read(BUFFER_SIZE_SEND)
            s.sendto(data, (HOST, PORT))
        except socket.error:
            pass


if __name__ == '__main__':
    main()
