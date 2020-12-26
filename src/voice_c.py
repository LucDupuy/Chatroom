import socket
import threading
# HOST = 0.0.0.0
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048
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
            msg = client_sock.recvfrom(BUFFER_SIZE)
            if len(msg) > 0:
                print(msg)
        except socket.error:
            pass


read_thread = threading.Thread(target=recv_data)
read_thread.start()

write_thread = threading.Thread(target=send_data)
write_thread.start()