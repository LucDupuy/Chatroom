import socket
import pyaudio
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 80
NUM_CONNECTIONS = 5
BUFFER_SIZE = 2048

BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(NUM_CONNECTIONS)

clients = []



def handle(client, stream):
    while True:
        mic_in = stream.read(BUFFER_SIZE)

        for client in clients:
            client.send(mic_in)


def server():
    p = pyaudio.PyAudio()
    stream = p.open(format=BIT_DEPTH, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER_SIZE)


    try:
        client, address = s.accept()
    except socket.error:
        TIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("Keyboard Interruption: Voice Channel closing.\n" + TIME)
        exit(0)


    clients.append(client)


    handle_thread = threading.Thread(target=handle, args=(client, stream))
    handle_thread.start()


if __name__ == '__main__':
    server()