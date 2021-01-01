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


def main():
    p = pyaudio.PyAudio()
    in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=-False, output=True, frames_per_buffer=BUFFER_SIZE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    get_thread = Thread(target=get_data, args=(in_stream, sock, ))
    send_thread = Thread(target=send_data, args=(sock, ))
    get_thread.start()
    send_thread.start()


def get_data(stream, server_sock):
    while True:
        data, address = server_sock.recvfrom(BUFFER_SIZE)
        stream.write(data)


def send_data(server_sock):
    while True:
        data, address = server_sock.recvfrom(BUFFER_SIZE)
        server_sock.sendto(data, address)


if __name__ == '__main__':
    main()

