import socket
import pyaudio
import threading
import tkinter.messagebox

# HOST = socket.gethostbyname("ilkka.ddns.net")
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
p = pyaudio.PyAudio()
in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=False, frames_per_buffer=BUFFER_SIZE)
out_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=False, output=True, frames_per_buffer=BUFFER_SIZE)


try:
    server_sock.connect((HOST, PORT))
except:
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.withdraw()
    tkinter.messagebox.showinfo("Error", "Server is offline")
    exit(0)


def client():
    while True:
        try:
            msg = server_sock.recv(BUFFER_SIZE)
            # Seeing what the server has to say
            out_stream.write(msg)
        except socket.error:
            server_sock.close()
            exit(0)


def send_data():
    while True:
        try:
            mic_in = in_stream.read(BUFFER_SIZE)
            server_sock.sendto(mic_in, (HOST, PORT))
        except socket.error as e:
            server_sock.close()
            print(e)
            exit(0)


read_thread = threading.Thread(target=client)
read_thread.start()

write_thread = threading.Thread(target=send_data)
write_thread.start()
