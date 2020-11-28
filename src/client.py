import socket
import threading

HOST = socket.gethostname()
PORT = 1127
BUFFER_SIZE = 1024

# IPV4, TCP
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.connect((HOST, PORT))
username = input("Please enter your username: ")


def client():
    while True:
        try:
            msg = server_sock.recv(BUFFER_SIZE).decode()
            if msg == "USERNAME":
                server_sock.send(username.encode())
            else:
                # Seeing what the server has to say
                print(msg)
        except:
            print("Error occurred.")
            server_sock.close()
            break




def send_data():

    while True:
        msg = f'{username}: {input()}'
        server_sock.send(msg.encode())


read_thread = threading.Thread(target=client)
read_thread.start()

write_thread = threading.Thread(target=send_data)
write_thread.start()