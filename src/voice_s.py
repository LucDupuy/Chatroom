import socket
import pyaudio
import threading

HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
server_sock = socket.socket()
clients = []

BUFFER_SIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER_SIZE)


def client_listener(host_socket):
    while True:
        try:
            # THIS IS THE PROBLEM LINE
            connection, address = host_socket.accept()
            clients.append(connection)
        except socket.error as e:
            print(e)
            exit(0)


def server():
    try:
        server_sock.bind((HOST, PORT))
        server_sock.listen()

        client_listener_thread = threading.Thread(target=client_listener, args=(server_sock,))
        client_listener_thread.start()

        while True:
            mic_in = stream.read(BUFFER_SIZE)

            for client in clients:
                client.send(mic_in)
    except socket.error as error:
        print(str(error))


if __name__ == '__main__':
    server()

# TODO: Currently this is TCP, not UDP
# TODO: Deal with multiple clients
