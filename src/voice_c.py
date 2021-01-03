import socket
import pyaudio
import threading

HOST = socket.gethostbyname("ROGUEONE")
PORT = 1128

BUFFER_SIZE_SEND = 1024
BUFFER_SIZE_RECEIVE = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

MY_IP = socket.gethostbyname(socket.gethostname())

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((HOST, PORT))

    p = pyaudio.PyAudio()
    in_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=BUFFER_SIZE_SEND)
    out_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=BUFFER_SIZE_SEND)


    get_event = threading.Event()
    get_event.set()

    send_event = threading.Event()
    send_event.set()


    get_thread = threading.Thread(target=get_data, args=(sock, in_stream, get_event))
    get_thread.daemon = True
    send_thread = threading.Thread(target=send_data, args=(sock, out_stream, send_event))
    send_thread.daemon = True

    get_thread.start()
    send_thread.start()

    return get_event, send_event, get_thread, send_thread


def get_data(s, stream, event):
    while event.is_set():
        try:
            data, addr = s.recvfrom(BUFFER_SIZE_RECEIVE)

            if addr[0] is MY_IP:
                stream.write(data)
        except socket.error as e:
            print(e)
            pass


def send_data(s, stream, event):
    while event.is_set():
        try:
            data = stream.read(BUFFER_SIZE_SEND)
            s.sendto(data, (HOST, PORT))
        except socket.error:
            pass


if __name__ == '__main__':
    main()
