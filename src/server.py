import socket
import threading
import pyaudio
import esky
import sys
from datetime import datetime




HOST = "0.0.0.0"
PORT = 1127
NUM_CONNECTIONS = 5
BUFFER_SIZE = 1024
DATETIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


clients = []
usernames = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(NUM_CONNECTIONS)
print("\n\n" + DATETIME)
print("--------------------")
print("\nServer listening.....")



def send_data_to_select_people(msg, idx, only_current):
    for client in clients:
        if only_current:
            if clients.index(client) == idx:
                client.send(msg)
        else:
            if clients.index(client) != idx:
                client.send(msg)


def send_data(msg):
    for client in clients:
        client.send(msg)


def handle(client):
    while True:
        try:
            data = client.recv(BUFFER_SIZE)
            if data.decode().__contains__("#users"):
                send_data_to_select_people(list_online().encode(), clients.index(client), only_current=True)
            else:
                send_data_to_select_people(data, clients.index(client), only_current=False)
        except:
            client_idx = clients.index(client)
            del clients[client_idx]
            client.close()
            username = usernames[client_idx]
            data = f'{username} left the chat.'

            send_data(data.encode())
            del usernames[client_idx]
            break


def server():
    while True:
        try:
            client, address = s.accept()
            client.send("USERNAME".encode())
        except:
            TIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print("Keyboard Interruption: Server closing.\n" + TIME)
            exit(0)
        try:
            username = client.recv(1024).decode()
            usernames.append(username)
        except:
            print("User closed connection")
            continue

        clients.append(client)


        send_data(f"{username} has joined the chat.".encode())

        send_data_to_select_people(list_online().encode(), clients.index(client), only_current=True)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def list_online():
    data = ""
    data += "\nUsers Currently Online\n"
    data += "**********************\n"
    for username in usernames:
        data += username + "\n"

    return data


if __name__ == '__main__':
    server()


# TODO: Implement Voice
# TODO: How to push updates?
# TODO: Message from another shouldn't interrupt your typing
# TODO: Suppress not a trusted source from windows
