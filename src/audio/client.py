import socket
import pyaudio
import tkinter
import tkinter.messagebox

# HOST = socket.gethostbyname("ilkka.ddns.net")
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
CHUNK = 2048
BIT_DEPTH = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def client(stream):
    try:
        client_sock.connect((HOST, PORT))
    except socket.error:
        root = tkinter.Tk()
        root.overrideredirect(1)
        root.withdraw()
        tkinter.messagebox.showinfo("Error", "Error connecting to voice channel")
        exit(0)

    while True:
        data = client_sock.recv(CHUNK)
        stream.write(data)


def main():

    # Audio
    p = pyaudio.PyAudio()

    stream = p.open(format=BIT_DEPTH, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    client(stream)



