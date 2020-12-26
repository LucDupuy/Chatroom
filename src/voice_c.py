import socket
import threading
import pyaudio

HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

#p = pyaudio.PyAudio()
#in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=False, frames_per_buffer=BUFFER_SIZE)
#out_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=False, output=True, frames_per_buffer=BUFFER_SIZE)

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def send_data():

    while True:
        try:
            msg = input()
            client_sock.sendto(msg.encode(), (HOST, PORT))
        except socket.error as e:
            client_sock.close()
            print(e)
            exit(0)



def recv_data():
    while True:

        try:
            msg_and_address = client_sock.recvfrom(BUFFER_SIZE)
            msg = msg_and_address[0]
            if len(msg) > 0:
                print(msg.decode())
        except socket.error:
            pass


read_thread = threading.Thread(target=recv_data)
read_thread.start()

write_thread = threading.Thread(target=send_data)
write_thread.start()
