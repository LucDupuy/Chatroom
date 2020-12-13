import socket
import pyaudio
import threading
import tkinter
import tkinter.messagebox

# HOST = socket.gethostbyname("ilkka.ddns.net")
SERVER_HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048
BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.bind((SERVER_HOST, PORT))


def get_data():

    while True:
        try:
            data, _ = client_sock.recvfrom(BUFFER_SIZE)
            print(data.decode())
        except socket.error:
            pass



def client():
    p = pyaudio.PyAudio()

    stream = p.open(format=BIT_DEPTH, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=BUFFER_SIZE)

    while True:
        data = client_sock.recv(BUFFER_SIZE)
        stream.write(data)




read_thread = threading.Thread(target=client)
read_thread.start()


write_thread = threading.Thread(target=get_data)
write_thread.start()

