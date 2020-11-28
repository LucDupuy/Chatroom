import socket
import threading
from pynput.keyboard import Key, Listener

HOST = socket.gethostname()
PORT = 1127
NUM_CONNECTIONS = 3
BUFFER_SIZE = 1024

clients = []
usernames = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(NUM_CONNECTIONS)


def handle(client):
    while True:
        try:
            data = client.recv(BUFFER_SIZE)
            send_data(msg=data)
        except:
            client_idx = clients.index(client)
            clients.remove(client_idx)
            username = usernames.index(client_idx)
            data = "", username, " left the chat.".encode()
            send_data(data)
            usernames.remove(client_idx)
            break


def send_data(msg):
    for client in clients:
        client.send(msg.encode())


def server():

    while True:
        client, address = s.accept()
        print(f"{address} has connected.")
        client.send("USERNAME".encode())
        username = client.recv(1024).decode()
        usernames.append(username)
        clients.append(client)

        send_data(f"{username} has joined the chat.")
        client.send("Connected to server".encode())


        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()


if __name__ == '__main__':
    server()
